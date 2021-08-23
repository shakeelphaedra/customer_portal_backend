from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from customer_dashboard.serializers import UserSerializer
from customer_dashboard.query import connect_to_server
from customer_dashboard.models import User
from django.contrib.auth import authenticate
#    import pdb
#    pdb.set_trace()

class DispatchLoginSerializer(TokenObtainPairSerializer):
   
   def validate(self, attrs):
       #intercept here to check username or email in attrs
       #replace username or phone with email 
       try:
           user = User.objects.get(email=attrs['email'])
           if user.user_type != 'Employee':
               return {"error": "You are not allowed to login."}
       except User.DoesNotExist as e:
           #if user does not exist query the esc
           #create new user and save it
            print(e)
            email = attrs['email']
            password = attrs['password']
            con = connect_to_server()
            
            if con:
                cursor = con.cursor()
                query = f"""select e.EmpNo,e.Email, e.FirstName, e.LastName, u.Password from Employee as e
                            join Users as u on e.EmpNo = u.TechID where u.Password = '{password}' and e.Email = '{email}'"""
                res = cursor.execute(query)
                res = res.fetchone()
                con.close()
                if res:
                    user = User.objects.create_user(email=attrs['email'],password=attrs['password'])
                    user.emp_no = res[0]
                    user.first_name = res[2]
                    user.last_name = res[3]
                    user.user_type='Employee'
                    user.save()
                    
       

       data = super().validate(attrs)
       self.get_token(self.user)
       data['employee_id'] = UserSerializer(self.user).data['emp_no']
       data['user_id'] = user.id
       data['full_name'] = self.user.first_name +' '+ self.user.last_name
       return data


       