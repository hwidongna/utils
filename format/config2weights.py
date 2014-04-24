import sys
from configparser import SafeConfigParser

if __name__=="__main__":
    config = SafeConfigParser()
    config.readfp(sys.stdin)
    fw = {}
    for section in config.sections():
        for name, value in config.items(section):
            if name == "features":
                features = value.split()
            if name == "weights":
                weights = value.split()
        fw.update(list(zip(features, weights)))
    sys.stdout.write(" ".join(fw[name] for name in 
        [name for name in sorted(fw) if not name.startswith("!")]))
