import pysoem
import sys
import time


def do_eoe_example(ifname):
    master = pysoem.Master()

    master.open(ifname)

    try:
        if master.config_init() > 0:
            # Assign IP addresses to each slave
            for slave_pos, slave in enumerate(master.slaves):
                slave.eoe_set_ip("10.12.34.%d"%(2 + slave_pos))
            # Start virtual network
            master.eoe_start_network("10.12.34.1", netmask="255.255.255.0")

            print("[   mac    ,   ip    , netmask ,  gateway , dns_ip , dns_name]")
            for s in master.slaves:
                print(s.eoe_get_ip())

            print("EOE network started. Use ctrl+c to exit")
            while True:
                # EOE requires mailbox service. Loop here to do that
                for s in master.slaves:
                    try:
                        wkc = s.mbx_receive()
                    except Exception as e:
                        print("Mail failure: " + e.__str__())
                        time.sleep(0.100)
                time.sleep(0.010)
        else:
            print('no slave available')
    except Exception as ex:
        raise ex
    finally:
        master.close()


if __name__ == '__main__':

    print('script started')

    if len(sys.argv) > 1:
        do_eoe_example(sys.argv[1])
    else:
        print('usage: python eoe_example.py <ifname>')
        print('avalible interfaces:')
        for interface in pysoem.find_adapters():
            print("  " + interface.name)
