from ..models import Player
from django.http import HttpResponse

def barca_squad(request):
    starting_players = Player.objects.filter(id__range=(2, 12)).order_by('id')
    bench_players = Player.objects.filter(id__range=(13, 23)).order_by('id')

    lines = []
    lines.append("</br>//// Barcelona Starting lineup ////")
    print("\n//// Barcelona Starting lineup ////")
    for p in starting_players:
        line = f"{p.number}. {p.name} ({p.position})"
        lines.append(line)
        print(line)

    lines.append("</br>//// Barcelona Bench ////\n")
    print("\n//// Barcelona Bench ////")
    for p in bench_players:
        line = f"{p.number}. {p.name} ({p.position})"
        lines.append(line)
        print(line)

    body = "<br>".join(lines)
    return HttpResponse(body)
