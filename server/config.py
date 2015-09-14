import os
import ConfigParser

CONFIG_PATH = "config.cfg"
KEY_LENGTH = 128

config_error = False
# if config does not exits
if os.path.isfile(CONFIG_PATH) == False:
    try:
        import binascii
        print ("[info]   config file does not exists!")
        file = open(CONFIG_PATH, "w")
        file.write("""[server]\nport=8888\n\n[API]\nkey=%s\ndefault_steps=24\n\n[database]\ntype=sqlite\npath=sqlite.db\n""" % str(binascii.b2a_hex(os.urandom(KEY_LENGTH/2))))
        file.close()
        print ("[info]   Please check the config at '" + CONFIG_PATH + "'!")
        os._exit(1);
    except Exception as e:
        print ("[error]  cannot create \"%s\" because %s" % (CONFIG_PATH, e))
        os._exit(1);


configParser = ConfigParser.RawConfigParser()
configParser.read(CONFIG_PATH)
try:
   server_port = configParser.get("server", "port")
   api_key = configParser.get("API", "key")
   default_steps = configParser.get("API", "default_steps")
   db_type = configParser.get("database", "type")
   db_path = configParser.get("database", "path")
except:
    print ("[error]  Please check the config at '" + CONFIG_PATH + "'!")
    os._exit(1);
