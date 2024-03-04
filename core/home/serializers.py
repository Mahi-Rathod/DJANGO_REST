from rest_framework import serializers
from .models import *

class StudentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Students
        # fields = ['name','age']
        # exclude = ['id',]
        fields = '__all__'
    
    def validateName(self,name):
        for x in name:
            if x.isdigit():
                raise serializers.ValidationError({"Error": f"name and fathername field should have only characters"})

    def validate(self, data):
        if data['age'] <18 :
            raise serializers.ValidationError({"Error":"age cannot be less than 18"})
        
        self.validateName(data['name'])
        self.validateName(data['father_name'])
        
        return data