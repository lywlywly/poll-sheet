from students.models import Entry, Choice

e = Entry.objects.all()

for _ in e:
    # if e.text == "Engagement":
    if len(Choice.objects.all().filter(poll=_)) == 0:
        Choice(poll=_, choice_text="1").save()
        Choice(poll=_, choice_text="2").save()
        Choice(poll=_, choice_text="3").save()
        Choice(poll=_, choice_text="4").save()
        Choice(poll=_, choice_text="5").save()

