if __name__ == "__main__":
    from pygame import *
    from evolutionary_neural_creature import creature
    from lib.game_world import world_map
    import pickle, random

    gameWorld = world_map.WorldMap(100, 100, 16, 0.35)

    creature1 = creature.Creature(random.randint(0,100), random.randint(0,100))

    record_age = creature1

    gameWorld.creatures.append(creature1)

    screen  =display.set_mode((1000, 1000))
    running = True
    clockity = time.Clock()
    passed_time = 0
    try:
        while running:
            for e in event.get():
                if e.type == QUIT:
                    running = False
            gameWorld.update()

            if len(gameWorld.creatures) == 0:
                gameWorld.creatures.append(creature.Creature(random.randint(0,100), random.randint(0,100)))
            oldest_generation = -1
            oldest_age = None
            for i in gameWorld.creatures:
                if oldest_age is None:
                    oldest_age = i
                else:
                    if i.age > oldest_age.age:
                        oldest_age = i
                oldest_generation = max(oldest_generation, i.generation)

            if oldest_age.age > record_age.age:
                record_age = oldest_age

            screen.blit(gameWorld.draw(10), (0,0))
            draw.circle(screen, (255,0,0), (int(oldest_age.x*10), int(oldest_age.y*10)), int(oldest_age.radius*10)+5, 2)
            display.flip()
            display.set_caption("FPS: %-6.2f | Year: %.2f"%(clockity.get_fps(), passed_time/365))
            passed_time+=1
            clockity.tick(0)
            print("Count: %03d Oldest: %05d Record: %05d Oldest generation: %02d"%(len(gameWorld.creatures), oldest_age.age, record_age.age, oldest_generation))
    finally:
        with open("record.enc", 'wb') as f:
            pickle.dump(record_age, f)
        with open("oldest.enc", 'wb') as f:
            pickle.dump(oldest_age, f)