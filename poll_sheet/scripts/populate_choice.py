from students.models import Entry, Choice

e = Entry.objects.all()
for _ in range(1, 13):
    if e[_ - 1].type == "choices_num":
        Choice(poll=e[_ - 1], choice_text="1").save()
        Choice(poll=e[_ - 1], choice_text="2").save()
        Choice(poll=e[_ - 1], choice_text="3").save()
        Choice(poll=e[_ - 1], choice_text="4").save()
        Choice(poll=e[_ - 1], choice_text="5").save()
    elif e[_ - 1].type == "text":
        Choice(poll=e[_ - 1], choice_text="Enter your words").save()
