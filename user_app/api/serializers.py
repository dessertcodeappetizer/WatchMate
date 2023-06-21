from django.contrib.auth.models import User
from rest_framework import serializers

class registrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}
        
    def save(self):                                                                 #In django we can use same email or password so to distinguish and to validate if each user have its unique email or not we are checking this
        
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:                                                    #Checking if the password is different
            raise serializers.ValidationError({'error': 'P1 and P2 should be same!'})
        
        if User.objects.filter(email=self.validated_data['email']).exists():         #If someone else id using the same email or not
            raise serializers.ValidationError({'error': 'Email already in use'})
        
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        
        return account
            