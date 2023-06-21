from rest_framework import serializers
from watchlist_app import models

class reviewserielizer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = models.Review
        exclude = ('watchli',)
        # fields = '__all__'


class watchlistSerializer(serializers.ModelSerializer):                            #model serializer is initiated like this
    # len_name = serializers.SerializerMethodField()                               #We can add one custom field without defining it inside the model
    # reviews = reviewserielizer(many=True, read_only=True)
    platform = serializers.CharField(source="platform.name")                      #To view platform name instead of platform id
                                                                                   
    class Meta:
        model = models.watchlist
        fields = '__all__'
        # fileds = ['name', 'description']                                        #It will not include all the fields only selected fields are included
        # exclude = ['name']                                                      #name will be excluded. Remember to give variable name as exclude and fields when used

class streamplatformSerializer(serializers.ModelSerializer):
    watchlist = watchlistSerializer(many=True, read_only=True)                    #In model we have made on var inside watchlist called platform inside platform we have taken "watchlist" as our related_name
                                                                                  #Here we are creating nested relationship where in one platform all their movie names are mentioned
    #watchlist = serializers.StringRelatedField(many=True)                        #It will paas only name of the movies
    #watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)   #You will get only pk
    #watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='movie-detail')
                                                                                 
    class Meta:
        model = models.streamplatform
        fields = '__all__'

                                                    
        
    # def get_len_name(self, object):                                              #name format is get_name of the variable
    #     return len(object.name)
    
    # def validate(self, data):
    #     if data['name'] == data['description']:                                   #Object level validation. Since we are checking all the fields of the object
    #         raise serializers.ValidationError('Name and description cannot be the same')
    #     return data
            
    # def validate_name(self, value):                                               #validate_entityname then name length will be checked
    #     if len(value) < 3:                                                        #This is field level validation since we are checking a particular field
    #         raise serializers.ValidationError("Name must be at least 3 characters long")
    #     return value   


# def name_length(self, value):
#     if len(value) < 3:
#         raise serializers.ValidationError("Name must be at least 3 characters")
#     return value

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
    ## name = serializers.CharField(validators=[name_length])                       #Third type of validation (Validator)
    # name = serializers.CharField()                       
    # description = serializers.CharField()
    # active = serializers.BooleanField()
    
    # def create(self, validated_data):                                             #This method used to create the object
    #     return Movie.objects.create(**validated_data)
    
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)                 #instance.name is the new name which will be updated by validated data
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.active = validated_data.get('active', instance.active)
    #     instance.save()
    #     return instance
    
    # def validate(self, data):
    #     if data['name'] == data['description']:                                   #Object level validation. Since we are checking all the fields of the object
    #         raise serializers.ValidationError('Name and description cannot be the same')
    #     return data
            
    # def validate_name(self, value):                                               #validate_entityname then name length will be checked
    #     if len(value) < 3:                                                        #This is field level validation since we are checking a particular field
    #         raise serializers.ValidationError("Name must be at least 3 characters long")
    #     return value
    