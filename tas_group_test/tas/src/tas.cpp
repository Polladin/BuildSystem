
#include<iostream>

#include "common_lib/common_lib.h";
#include "utils/utils.h";
#include "common/common_net/common_net.h";
#include "common/libTCPPinger/libTCPPinger.h";
#include "common/http/client/client.h";
#include "common/http/server/server.h";
#include "xpdb/xpdb.h";
#include "phoneparser/phoneparser.h";


int main()
{
    std::cout << common_lib(10) << std::endl;
    std::cout << utils(10) << std::endl;
    std::cout << common_net(10) << std::endl;
    std::cout << libTCPPinger(10) << std::endl;
    std::cout << client(10) << std::endl;
    std::cout << server(10) << std::endl;
    std::cout << xpdb(10) << std::endl;
    std::cout << phoneparser(10) << std::endl;

    std::cin.get();

}