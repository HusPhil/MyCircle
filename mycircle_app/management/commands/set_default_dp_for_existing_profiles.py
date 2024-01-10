
from django.core.management.base import BaseCommand
from mycircle_app.models import Profile, ProfilePicture

class Command(BaseCommand):
    help = 'Create default profile pictures for profiles without an associated picture'

    def handle(self, *args, **options):
        profiles_without_picture = Profile.objects.exclude(profile_picture__isnull=False)
        default_picture_path = 'blank_img.png'

        for profile in profiles_without_picture:
            default_profile_picture = ProfilePicture.objects.create(user_profile=profile, img=default_picture_path)
            self.stdout.write(self.style.SUCCESS(f"Created default picture for profile: {profile.pk}"))
