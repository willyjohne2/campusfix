from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile


class Command(BaseCommand):
    help = "Sync user roles from is_staff/is_superuser to the new role field"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be changed without making changes",
        )

    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False)

        # Get all users and check their profile roles
        users = User.objects.all()
        updated_count = 0
        unchanged_count = 0

        for user in users:
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                # Create profile if it doesn't exist
                profile = Profile.objects.create(
                    user=user, name=user.get_full_name() or user.username
                )
                self.stdout.write(
                    self.style.WARNING(f"Created missing profile for {user.username}")
                )

            # Determine role based on is_staff and is_superuser
            current_role = profile.role

            if user.is_superuser:
                new_role = "superadmin"
            elif user.is_staff:
                new_role = "admin"
            else:
                new_role = "user"

            if current_role != new_role:
                if not dry_run:
                    profile.role = new_role
                    profile.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"{user.username}: {current_role} → {new_role}"
                        )
                    )
                else:
                    self.stdout.write(
                        f"{user.username}: {current_role} → {new_role} (DRY RUN)"
                    )
                updated_count += 1
            else:
                unchanged_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Complete! Updated: {updated_count}, Unchanged: {unchanged_count}"
            )
        )
