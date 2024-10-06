from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver

from .models import User, UserProfile



@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender,instance,created, **kwargs):
    # Next step is to connect the receiver to the sender here sender is User
    # we can connect sender and receiver in the below way or simply use decorator
    #post_save.connect(post_save_create_profile_receiver, sender=User)

    if created:
        # write code to create user profile as soon as the user is created
        UserProfile.objects.create(user=instance)
        print("User profile is created")
    
    else:
        try:
            '''profile = User.objects.get(user=instance)
            profile.save()
            print("User is updated")'''
            instance.userprofile.save()
        except:
            # Create the user incase if the previously created profile deleted
            UserProfile.objects.create(user=instance)
            print("Profile was not exist, but created")


# presave will not take receiver flag it will trigger before profile is created 
@receiver(pre_save,sender=User)
def pre_save_profile_receiver(sender,instance, **kwargs):
    print(instance.username,"This user is being created")
