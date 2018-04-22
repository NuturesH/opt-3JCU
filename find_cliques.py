#!-*-coding:UTF-8-*-
############################
#**#Nutures
#**#2018/4/16
#**#在网络中寻找全连接网络
#**#从子网中写出全网络列表
#**#根据子网来写出网络列表
import networkx as nx
from networkx.algorithms.community.kclique import k_clique_communities
#输入文件X， 输出文件Y，输出的全连接网络的列表Y2，全连接节点数K
def find_cliques(X, Y, Y2, K):
    #将文件X转换为图，并将X放入列表
    def G_graph(X):
        G_list = []
        G = nx.Graph()
        fp = open(X, 'r')
        #将文件写入图，和列表
        for line in fp:
            if 'o p i' not in line:
                G_list.append(line.strip())
                G.add_edge(line.strip().split()[0], line.strip().split()[1])
        print '输入网络边的数目：',len(G_list)
        return G_list, G

    #发现X网络中K个节点的全连接网络所包含的节点
    def connected_network(X,K):
        G_list, G = G_graph(X)
        K_net = []
        #寻找G网络中全连接网络
        con_net = list(nx.find_cliques(G))
        #将K个节点的全连接网络所包含的节点加入列表
        for net in con_net:
            if len(net) == int(K):
                #print net
                K_net.append(net)
        print str(K)+'个节点的全连接网络数目为：',len(K_net)
        return G_list, K_net

    #发现X网络中K个节点的社区所包含的节点
    def find_community(X, K):
        G_list, G = G_graph(X)
        K_net = []
        #寻找社区
        comnity = list(k_clique_communities(G, K))
        #将社区节点加入网络：
        for net in comnity:
            if len(net) > K:
                K_net.append(net)
        print str(K) + '个节点所包含社区中的全连接网络为：',len(K_net)
        return G_list, K_net

    #根据全连接网络的所包含的节点数来写全连接网络,或者社区
    def make_network(X, Y, Y2, K, num):
        if num == 0:
            G_list, K_net = connected_network(X, K)
        if num == 1:
            G_list, K_net = find_community(X, K)
            print K_net
        node_edg = []
        #将全连接的节点写入文件
        fd = open(Y2, 'w')
        for i in K_net:
            print >> fd, '[ ' + " ".join(i) + ' ]'
        fd.close()
        #写全连接网络
        fp = open(Y,'w')
        print >> fp, 'o p i'
        #根据边来寻找权重并写入网络
        for lt in K_net:
            for i in lt:
                for j in lt:
                    for line in G_list:
                        l_list = line.split()
                        if i in l_list and j in l_list and line not in node_edg and i != j:
                            node_edg.append(line)
                            break

        print '全连接网络边的数目：',len(node_edg)
        for i in node_edg:
            print >> fp, i
        fp.close()
        return 0
    make_network(X, Y, Y2, K, 0)
find_cliques('./start/all_res/N0_0.001/all_res_N0_0.001_chain.dat', './start/all_res/N0_0.001/5/connect/5connect_all.dat', './start/all_res/N0_0.001/5/connect/5connect_list_all.dat', 5)
#find_cliques('./AB/AB/N0_0.001/AB_N0_0.001_chain.dat', './AB/AB/N0_0.001/5/connect/5connect_AB.dat', './AB/AB/N0_0.001/5/connect/5connect_list_AB.dat', 5)
#find_cliques('./start/res_res/N0_0.001/res_res_N0_0.001_chain.dat', './start/res_res/N0_0.001/5/5connect_res.dat', './start/res_res/N0_0.001/5/5connect_list_res.dat', 5)


#根据子网节点选择全连接的网络， 子网的节点，网络的全连接列表
def find_list(X1, X2, Y):
    #将子网的节点写入文件，全连接列表也写入文件
    def inp_f(X1, X2):
        node_list = []
        connect_list = []
        [node_list.append(line.strip()) for line in open(X1) if True]
        [connect_list.append(line.strip()) for line in open(X2) if True]
        print str(X1) + "节点数目：", len(node_list)
        print str(X2) + "全网络个数：", len(connect_list)
        return node_list, connect_list
    #根据节点选出全连接的网络
    def find_con(X1,X2):
        node_list , connect_list = inp_f(X1, X2)
        con_list = []
        #根据节点寻找网络
        for node in node_list:
            for net in connect_list:
                if node in net:
                    net = "  ".join(net.split()[1:-1])
                    #print net
                    con_list.append(net)
                    break
        con_list = list(set(con_list))
        print str(X1) + "节点的全网络数目：" , len(con_list)
        return con_list
    #将网络写出
    def write_net(X1, X2, Y):
        con_list = find_con(X1, X2)
        fp = open(Y, 'w')
        for line in con_list:
            print >> fp, '[ ' + line + ']'
        fp.close()
    write_net(X1,X2,Y)

# find_list('/home/nutures/workspace/3JCU/opt_structure/date/start/all_res/N0_0.001/4/community/4community_all_OEC_sub1.dat',
#           '/home/nutures/workspace/3JCU/opt_structure/date/start/all_res/N0_0.001/4/connect/4connect_list_all.dat',
#           '/home/nutures/workspace/3JCU/opt_structure/date/start/all_res/N0_0.001/4/community/4connect_all_OEC_sub1_list.dat')
# find_list('/home/nutures/workspace/3JCU/opt_structure/date/AB/AB/N0_0.001/4/connect/4connect_AB_sub1.dat',
#           '/home/nutures/workspace/3JCU/opt_structure/date/AB/AB/N0_0.001/4/connect/4connect_list_AB.dat',
#           '/home/nutures/workspace/3JCU/opt_structure/date/AB/AB/N0_0.001/4/connect/4connect_AB_sub1_list.dat')




















