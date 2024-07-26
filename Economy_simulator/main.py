
from society import Society
from interface import GraphicInterface


main = Society()
GUI = GraphicInterface(main)

c = 0

while main.count_hungry() < 1:
    print('----------------')
    print('tick number ', c)
    print(main.count_hungry()) 
    main.tick() 
    main.market.print_infos()
    c += 1

main.count_professions()

GUI.main()