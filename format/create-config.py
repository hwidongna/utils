import ConfigParser, sys

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog source target alignment probfile [options] ")
    parser.add_option("-c", "--configfile", dest="configfile", help="moses configureation file as template")
    parser.add_option("-f", "--feature", dest="feature", help="feature template")
    parser.add_option("-w", "--weight", dest="weight", help="feature template")
    options, args = parser.parse_args()
    config = ConfigParser.SafeConfigParser(allow_no_value=True)
    config.optionxform = str
    config.readfp(open(options.configfile))
    for section in config.sections():
        if section.startswith("weight-"):
            config.remove_section(section)
    assert len(options.feature.split()) > 0 and len(options.weight.split()) > 0
    assert len(options.feature.split()) == len(options.weight.split())
    newsect = {}
    for feature, weight in zip(options.feature.split(), options.weight.split()):
        type, i = feature.split("_")
        newsect.setdefault(type[0].lower(),[]).append(weight)
    for section in newsect:
        config.add_section("weight-"+section)
        for weight in newsect[section]:
            config.set("weight-"+section, weight, "")
    config.write(sys.stdout)
