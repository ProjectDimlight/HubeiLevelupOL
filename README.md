# HubeiLevelupOL

## 游戏说明

### 游戏目标

- 游戏需要4个人，使用包含大小王在内的1副标准扑克牌。
- 坐在对侧的两人为同一阵营，在游戏开始时确定不再变化。
- 两个阵营的初始点数为【3】；每一盘升级游戏以率先“升级”到【A】为目标。
- 每一盘游戏包含若干局。每一局获胜的阵营可以升级，点数+1，且在下一局成为庄家。失败的阵营成为散家。

### 一局流程

- 确定庄家
    - 上一局庄家如果胜利，则本局庄家为上局庄家的队友；否则，本局庄家为上局庄家的下家（对手）。
        - 如果本局为第一局，则庄家由“叫牌”决定（见下节）。
    - 本局的主牌点数为当前庄家的点数。
- 摸牌与叫牌
    - 从庄家开始，每人按逆时针顺序依次摸一张牌。每人摸12张。
    - 在本阶段任何时刻，若还没有人叫牌，任意一名玩家可以展示一张等同于本局点数的牌，称为“叫牌”。
        - 本局的主牌花色此时确定为展示的牌的点数。（见例1）
        - 若本局为第一局，则叫牌的玩家成为庄家。
    - 如果在摸牌全部结束后，仍然没有玩家叫牌，则翻开底牌的第3张以确定主牌花色
        - 若第3张为大小王，则顺延至第4张或第5张
- 扣牌
    - 剩下的6张牌成为底牌，在摸牌结束后全部交给庄家。
    - 庄家选择6张牌，扣置为底牌。
- 打牌
    - 接下来进入打牌环节。每一轮中，上一轮获胜的玩家率先出牌，称为先手。
        - 若本轮为本局第一轮，则从庄家开始出牌。
    - 先手可以选择出：
        - 1张任意牌；
        - 若干张同花色的副牌（非主牌），称为顺子；顺子当中的每一张牌都必须要大于其余玩家（包括队友）手中所有同花色的牌，但是不要求连续。（见例2）
    - 其余的玩家按逆时针顺序依次出牌。
        - 必须出与先手相同数量的牌（因此在任意一轮结束时所有人的手牌数应相同）；
        - 若手中具有相同花色的牌，必须优先将所有相同花色的牌出完；
            - 所有主牌视为花色相同，且与其实际花色不同；
        - 若所有牌的花色与先手的花色相同，则称为跟牌，按照最大的那张牌计算牌的大小；
        - 若所有牌均为主牌，则称为杀牌，杀牌大于其他牌；若有多名玩家杀牌，按照最大的那张牌计算牌的大小；若有牌大小相等，则先出的牌较大；
        - 否则，称为垫牌（哪怕包含主牌），垫牌小于其他所有牌。（见例3）
    - 打出最大的牌的玩家获得本轮的胜利，获得所有分牌对应的分数，并且下一轮先手。
- 结算
    - 当所有玩家打完所有牌时，本局结束。
    - 若散家获得至少40分，或者在最后一轮当中胜利（称为抠底），散家胜，下一局成为庄家；否则庄家胜，庄家升级。
        - 若散家抠底，则散家获得底牌中的所有分数乘2。
        - 若散家获得60分、80分可以在成为庄家的基础上额外升1、2级。
        - 若庄家获胜且散家获得0分，则庄家额外升2级。

### 牌

- 主牌
    - 主牌的点数由庄家等级确定。主牌的花色由叫牌决定。
    - 所有点数等于庄家等级（级主）、或者花色等于叫牌花色的牌，以及所有2牌（2主）、王牌，称为主牌
        - 其中，花色等于叫牌花色的级主和2主称为本级和本2，分别大于其他级主和2主
        - 大小关系为：大王>小王>本级主>其他级主>本2>其他2>主A>主K>...>主3（当然，其中跳过级主）
- 副牌
    - 所有不是主牌的牌为副牌。
    - 相同花色的牌可以比较大小关系；后出的不同花色的牌称为垫牌，视为最小
        - 相同花色大小关系为：A>K>...（跳过级主）>3
- 分牌
    - 所有5、10、K（无论是否是主牌）都是分牌。一副牌中一共100分。
        - 5：计5分
        - 10：计10分
        - K：计10分

### 例子

- 例1
    - 本局庄家为玩家0，等级为3。
    - 玩家0、1、2、3各摸到5张牌，轮到玩家0摸牌，获得一张♥3。
    - 玩家0叫牌，本局的主牌花色确定为♥。
- 例2
    - 本轮轮到玩家2先手。
    - 玩家2手中有♠A，♠K，♠J。
    - 若此时玩家3手中有♠Q，则玩家2【不可以】打出顺子♠A，♠K，♠J。
        - 但是可以打出♠A，♠K。
    - 若♠Q曾经被打出或者被扣置为底牌，则玩家2可以打出顺子♠A，♠K，♠J。
- 例3
    - 本局主牌点数为3，花色为♦。
    - 玩家1先手，打出顺子♠A，♠K。
    - 玩家2手中没有♠，选择杀牌，打出♠2，♦J（两张均为主牌，♠2因为是主牌所以不计为♠牌）。
    - 玩家3为了保护分数选择杀牌，打出♦2，♦5（由于♦2是本2，所以即便是后出，也仍然大于♠2；另外，此处只比较最大的那张牌的点数，对♦J和♦4不做比较）。
    - 玩家4由于手中有♠，选择垫牌，打出♠6，♣7（包含不同花色只能作为垫牌，视为最小）。
    - 本轮玩家3获胜；玩家1、玩家3阵营获得♠K和♦5总计15分。

## 部署（Todo）

- build frontend
- deploy backend
- play on browser