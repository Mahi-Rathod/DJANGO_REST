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
    
        if 'name' in data:
            self.validateName(data['name'])
            
        if 'father_name' in data:
            self.validateName(data['father_name'])
        
        return data
    
    
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        

class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer()    #it will pick foreign key from the Category Model
    class Meta:
        model = Book
        fields = '__all__'
        
    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category_instance, _ = Category.objects.get_or_create(**category_data)
        book_instance = Book.objects.create(category=category_instance, **validated_data)
        return book_instance
    
    def update(self,instance, data):
        Category_data = data.pop('category',None)
        if Category_data:
            category_instance = instance.category
            
            for key, value in Category_data.items():
                setattr(category_instance, key, value)
            category_instance.save()
        return super().update(instance, data)
        
    