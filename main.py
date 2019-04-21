def construct_graph(population_tracker, food_tracker):

    fig, ax1 = plt.subplots()

    ax1.set_xlabel("Time (Days)")
    ax1.set_ylabel("Population")
    ax1.plot(population_tracker, label='Population', color='tab:blue')

    ax2 = ax1.twinx()

    ax2.set_ylabel("Food")
    ax2.plot(food_tracker, label='Food', color="tab:orange")

    #fig.tight_layout()
    fig.legend(loc="lower right", ncol=2, bbox_to_anchor=(1,0), bbox_transform=plt.gcf().transFigure)
    plt.title("Population of Ballbois Over Time (%.2f year survey)" % (passed_time / 365))
    fig.show()


if __name__ == "__main__":
    from pygame import *
    from evolutionary_neural_creature import creature
    from lib.game_world import world_map
    import pickle, random
    import matplotlib.pyplot as plt

    gameWorld = world_map.WorldMap(100, 100, 16, 0.33)

    creature1 = creature.Creature(random.randint(0,100), random.randint(0,100))

    record_age = creature1

    gameWorld.creatures.append(creature1)

    population_tracker = []

    food_tracker = []

    screen  =display.set_mode((1000, 1000))
    running = True
    clockity = time.Clock()
    passed_time = 0
    try:
        while running:
            for e in event.get():
                if e.type == QUIT:
                    running = False
            food_tracker.append(gameWorld.update())

            while len(gameWorld.creatures) < 10:
                gameWorld.creatures.append(creature.Creature(random.randint(0,100), random.randint(0,100)))
            youngest_generation = -1
            oldest_age = None
            for i in gameWorld.creatures:
                if oldest_age is None:
                    oldest_age = i
                else:
                    if i.age > oldest_age.age:
                        oldest_age = i
                youngest_generation = max(youngest_generation, i.generation)

            if oldest_age.age > record_age.age:
                record_age = oldest_age

            screen.blit(gameWorld.draw(10), (0,0))
            draw.circle(screen, (255,0,0), (int(oldest_age.x*10), int(oldest_age.y*10)), int(oldest_age.radius*10)+5, 2)
            display.flip()
            display.set_caption("FPS: %-6.2f | Year: %.2f"%(clockity.get_fps(), passed_time/365))
            passed_time+=1
            clockity.tick(0)
            print("Count: %03d Oldest: %05d Record: %05d Youngest generation: %02d" % (len(gameWorld.creatures), oldest_age.age, record_age.age, youngest_generation))
            population_tracker.append(len(gameWorld.creatures))
    finally:
        with open("record.enc", 'wb') as f:
            pickle.dump(record_age, f)
        with open("oldest.enc", 'wb') as f:
            pickle.dump(oldest_age, f)


        construct_graph(population_tracker, food_tracker)
