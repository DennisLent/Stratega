import stratega

if __name__ == "__main__":

    config = stratega.load_config("resources/gameConfigurations/TBS/Original/KillTheKing.yaml")
    runner = stratega.create_runner(config)

    config_agents = stratega.generate_agents(config)

    resolution=stratega.Vector2i(1920,1080)
    runner.play(config_agents, resolution, 0)