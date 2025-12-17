from ..models import Player
from django.http import HttpResponse

def juve_squad(request):
    starting_players = Player.objects.filter(id__range=(23, 34)).order_by('id')
    bench_players = Player.objects.filter(id__range=(34, 41)).order_by('id')

    lines = []
    lines.append("</br>//// Juventus Starting lineup ////\n")
    print("\n//// Juventus Starting lineup ////")
    for p in starting_players:
        line = f"{p.number}. {p.name} ({p.position})"
        lines.append(line)
        print(line)

    lines.append("</br>//// Juventus Bench ////\n")
    print("\n//// Juventus Bench ////")
    for p in bench_players:
        line = f"{p.number}. {p.name} ({p.position})"
        lines.append(line)
        print(line)

    body = "<br>".join(lines)
    return HttpResponse(body)
