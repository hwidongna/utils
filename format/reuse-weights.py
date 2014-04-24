import sys
from configparser import SafeConfigParser

if __name__=="__main__":
    config = SafeConfigParser()
    config.readfp(open(sys.argv[1]))
    model = {}
    for section in config.sections():
        for name, value in config.items(section):
            if name == "features":
                for name in value.split():
                    model[name] = section

    newconfig = {}
    for name, weight in zip([name for name in sorted(model) if not name.startswith("!")], sys.stdin.readline().split()):
        newconfig.setdefault(model[name], {}).setdefault(name, weight)

    for section in newconfig:
        features, weights = list(zip(*list(newconfig[section].items())))
        config.set(section, "features", " ".join(features))
        config.set(section, "weights", " ".join(weights))

    config.write(sys.stdout)
