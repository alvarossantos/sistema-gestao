from django.utils import timezone


def hoje(request):
    """Context processor que disponibiliza 'hoje' em todos os templates."""
    return {"hoje": timezone.localdate()}
