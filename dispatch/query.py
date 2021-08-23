from customer_dashboard.query import connect_to_server
from customer_dashboard.custom_exception import (NotFoundError, ConnectionError,
                                                 ESCDataNotFetchingError)
from dispatch.custom_exception import DispatchUpdateError




def get_dispatches(emp_no):
    con = connect_to_server()
    if con:
        try:
            cursor = con.cursor()
            query = f"""select t.ServiceMan,c.Add1 as CustomerAddress, d.Dispatch,d.LocNo,t.TechTime,
                        d.CalledInBy, (c.FirstName+c.LastName) as CustomerName, c.Phone1, l.Longitude, l.Latitude
                        from Dispatch as d join DispTech as t
                        on d.Dispatch = t.Dispatch join Customer as c 
                        on d.CustNo = c.CustNo join Location as l
                        on d.LocNo = l.LocNo and d.CustNo = l.CustNo 
                        where t.ServiceMan={emp_no} and t.DispDate = '2021-01-22' order by t.DispTime"""

            res = cursor.execute(query)
            res = res.fetchall()
            # con.close()
            data_dict = {}
            if res:
                data = []
                total_time = 0
                total_price = 0
                for rec in res:
                    cursor = con.cursor()
                    query = cursor.execute(f"select SUM(Price) from DispParts where Dispatch = '{rec[2]}'")
                    price = query.fetchone()
                    if price[0]:
                        total_price+=float(price[0])
                    dic = {
                        'dipatch': rec[2],
                        'emp_no': rec[0],
                        'customer_address': rec[1],
                        'loc_no': rec[3],
                        'tech_time': rec[4],
                        'called_in_by': rec[5],
                        'customer_name': rec[6],
                        'phone': rec[7],
                        'longitude': rec[8],
                        'latitude': rec[9]
                    }
                    data.append(dic)
                    total_time += rec[4]
                con.close()
                data_dict['data'] = data
                data_dict['total_dispatches'] = len(res)
                data_dict['total_time'] = total_time
                data_dict['emp_no'] = emp_no
                data_dict['est_margin'] = total_price
            else:
                raise NotFoundError
        
            return data_dict
        except Exception as e:
            raise ESCDataNotFetchingError('Could not fetch data from database')
    else:
        raise ConnectionError


def get_dispatch_details(disp_no):
    con = connect_to_server()

    if con:
        try:
            cursor = con.cursor()
            query = f""" select (c.FirstName+c.LastName) as CustomerName, c.Add1,d.CalledInBy, d.LocNo, c.Phone1,
                            l.Longitude, l.Latitude, d.Dispatch, d.Notes, dt.Status, dt.TechTime from  Dispatch as d
                            join Location as l on d.LocNo = l.LocNo and d.CustNo = l.CustNo 
                            join Customer as c on d.CustNo = c.CustNo
                            join DispTech as dt on d.Dispatch = dt.Dispatch
                            where d.Dispatch = '{disp_no}' """

            res = cursor.execute(query)
            res = res.fetchone()
            data_dict = {}
            if res:
                data_dict['data'] = {
                                    'dispatch': res[7],
                                    'customer_name': res[0],
                                    'customer_address': res[1],
                                    'called_in_by': res[2],
                                    'loc_no': res[3],
                                    'phone': res[4],
                                    'longitude': res[5],
                                    'latitude': res[6],
                                    'notes': res[8],
                                    'status': res[9],
                                    'tech_time': res[10]
                                    
                                }
            
                res1 = cursor.execute(f"select SUM(Price) from DispParts where Dispatch = '{disp_no}' ")
                
                price = res1.fetchone()
                if price[0]:
                    data_dict['total_margin'] = float(price[0])
                else: 
                    data_dict['total_margin'] = 0.0
            else:
                raise NotFoundError
            con.close()
            return data_dict
        except Exception as e:
            raise ESCDataNotFetchingError('Could not fetch data from database')
    else:
        raise ConnectionError



def get_dispatch_parts(disp_no):
    con = connect_to_server()
    if con:
        try:
            cursor = con.cursor()
            query = f""" SELECT DispParts.[Prod],DispParts.[Desc],DispParts.[WH],
                         DispParts.[Price],DispParts.[Quan]
                         FROM DispParts WHERE DispParts.[Dispatch] = '{disp_no}' """

            res = cursor.execute(query)
            data_dict = {}
            data_dict['disp_no'] = disp_no
            if res:
                res = res.fetchall()
                con.close()
                data = []
                for record in res:
                    dic = {
                        'quantity': record[4],
                        'parts': record[0],
                        'description': record[1],
                        'warehouse': record[2],
                        'price': record[3]
                    }
                    data.append(dic)
                
                data_dict['data'] = data
                return data_dict

            else:
                raise NotFoundError

        except Exception as e:
            raise ESCDataNotFetchingError("Could not fetch the data from database")
    else:
        raise ConnectionError




def get_dispatch_invoices(cust_no):
    con = connect_to_server()
    if con:
        try:
            cursor = con.cursor()
            query = f""" Select Invoice, Dispatch, InvDate from Sales where CustNo = '{cust_no}'  """

            res = cursor.execute(query)
            data_dict = {}
            data_dict['cust_no'] = cust_no
            if res:
                res = res.fetchall()
                con.close()
                data = []
                for record in res:
                    data.append({
                        'dispatch_no': record[1],
                        'invoice_no': record[0],
                        'date_completed': record[2] 
                    })
                    
                
                data_dict['data'] = data
                return data_dict

            else:
                raise NotFoundError

        except Exception as e:
            raise ESCDataNotFetchingError("Could not fetch the data from database")
    else:
        raise ConnectionError




def check_note_availability(disp_no):
    con = connect_to_server()

    if con:
        cursor = con.cursor()
        query = f""" select AHSDispatch from Dispatch where Dispatch = '{disp_no}' """
        run = cursor.execute(query)
        res = run.fetchone()
        if res:
            if res[0] == 0:
                try:
                    query2 = f""" Update Dispatch set AHSDispatch = 1 where Dispatch = '{disp_no}' """
                    run = cursor.execute(query2)
                    cursor.commit()
                    con.close()
                    return False
                except Exception as e:
                    print(e)
            else:
                return True
        else:
            raise ESCDataNotFetchingError
    else:
        raise ConnectionError



def search_parts(part_name):
    con = connect_to_server()
    if con:
        try:
            cursor = con.cursor()
            query = f""" select Inven.[Part], Inven.[Desc], Inven.[Type] from Inven Where Part  Like '%{part_name}%' """
            run = cursor.execute(query)
            res = run.fetchall()
            data_dict = {}
            data = []
            if res:
                data_dict['total'] = len(res)
                for record in res:
                    data.append({
                        'Name': record[0],
                        'Description': record[1],
                        'Type': record[2]

                    })
                data_dict['data'] = data
                return data_dict
            else:
                raise NotFoundError
        except Exception as e:
            raise ESCDataNotFetchingError()
            
    else:
        raise ConnectionError


def update_dispatch_status(status, disp_no):
    con = connect_to_server()

    if con:
        
        query = f""" Update DispTech set Status = '{status}' where Dispatch = '{disp_no}' """
        cursor = con.cursor()
        update_status = cursor.execute(query)
        cursor.commit()
        con.close()
        return {'success': True}
        
    else:
        raise ConnectionError