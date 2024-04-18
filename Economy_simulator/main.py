
from society import Society

main = Society()


while main.count_hungry() < 1:
    main.tick() 
    main.market.print_infos()