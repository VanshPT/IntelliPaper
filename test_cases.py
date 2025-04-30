test_cases = [
    LLMTestCase(
        input="Could you walk me through the three‑stage matching algorithm the authors implement in their continuous double‑auction market?",
        actual_output="""The matching engine in the continuous double-auction market uses a three-stage algorithm:
Stage 1: Order Book Population: Incoming limit orders (orders to buy or sell at a specific price or better) that don't immediately find a match are added to the order book. The order book is organized using price-time priority, meaning the best prices are matched first, and if multiple orders exist at the same price, the oldest order is prioritized.
Stage 2: Market Order Processing: Market orders (orders to buy or sell at the best available price) are processed in two steps:
(a) Market-to-Market Matching: Market buy orders are matched with market sell orders at the current market price. These orders are essentially netted against each other.
(b) Market-to-Book Matching: Any remaining market orders are then matched against existing limit orders in the order book.
Stage 3: Crossing Limit Order Matching: Any limit orders that cross the market (a buy order with a price higher than the best ask price or a sell order with a price lower than the best bid price) are matched against existing orders in the order book. This ensures that trades occur whenever possible.""",
        expected_output="""Orders are handled in three sequential phases: (1) non‑crossing limit orders join the book; (2a) market‑to‑market netting; (2b) market‑to‑book execution; (3) any still‑crossing limit orders are matched.""",
        context=[
            """The matching engine processes these orders
through three sequential phases:
First, incoming limit orders that do not immediately cross the market are added to
the order book, maintaining strict price-time priority. Second, market orders are processed
through a two-stage matching algorithm: (a) market-to-market matching, where market
orders are netted against each other at the current market price, and (b) market-to-book
matching, where remaining market orders are executed against standing limit orders. Finally,
any crossing limit orders are matched against the order book."""
        ],
        retrieval_context=[
            """value considerations.
In a double auction, buyers and sellers actively submit orders, with trades occurring when
compatible buy and sell orders match the price. The matching engine processes these orders
through three sequential phases:
First, incoming limit orders that do not immediately cross the market are added to
the order book, maintaining strict price-time priority. Second, market orders are processed
through a two-stage matching algorithm: (a) market-to-market matching, where market
orders are netted against each other at the current market price, and (b) market-to-book
matching, where remaining market orders are executed against standing limit orders. Finally,
any crossing limit orders are matched against the order book.
10
2.1.2 Implementation Details
The matching engine ( MatchingEngine class) implements three primary components that
work together to facilitate efficient market operation. The order processing component han-
dles the core matching functionality, where market orders are executed immediately against
the best available prices in the order book during each trading round. When immediate
execution is impossible, limit orders are stored in the order book according to price-time
priority. The system supports partial executions, maintaining careful tracking of remaining
quantities to ensure complete order fulfillment across multiple trades when necessary.
Position management forms the second critical component, providing comprehensive
tracking of agent positions and cash balances throughout the trading session. Before any
trade execution, the system performs rigorous pre-trade validation to ensure agents have suffi-
cient resources to fulfill their orders. This check includes validating buyer cash commitments
and shares availability for sellers, with the system maintaining accurate records of commit-
ted and available resources for each agent. The position management system updates in
real-time as trades are executed, ensuring market integrity and preventing over-commitment
of resources.
The price formation mechanism constitutes the third component, implementing a sys-
tematic price discovery and market monitoring approach. As trades are executed within each
round, the system dynamically updates prices based on executed trades while continuously
tracking market depth and bid-ask spreads. This data collection provides detailed insights
into market liquidity and efficiency. Each trade is logged with comprehensive information,
including price, quantity, and participating agents, creating a complete audit trail of mar-
ket activity. This comprehensive price formation system ensures transparent price discovery
while generating rich data for market quality analysis.
11
2.1.3 Extensibility Features
The framework employs a modular architecture to support diverse experimental configura-
tions and research objectives. At its foundation, the system implements configurable market
rules and trading constraints that can be adjusted to study different market conditions.
The asset model supports fundamental features like dividend payments and interest accrual,
enabling research across different market scenarios. Through its modular service-based ar-
chitecture, the trading mechanism layer allows for adaptation to other market structures
beyond the base double-auction system, such as call auctions or dark pools. Furthermore,
the framework provides flexible integration points for different LLM agent types and strate-
gies, allowing researchers to experiment with diverse behavioral models and decision-making
approaches.
This extensible design creates numerous research opportunities for market microstructure
studies. Researchers can systematically investigate how different market structures influence
price formation and efficiency, evaluate the impact of various trading rules on market qual-
ity, and analyze the complex interactions between different agent types and strategies. The""",
            """the second agents’ design, and the third the analysis module.
8
2.1 Market Design
Our methodological framework integrates three components that create a controlled envi-
ronment for LLM-based trading agents. The framework implements a flexible continuous
double-auction market mechanism that couples standard market microstructure principles
with market clearing and matching algorithms to accommodate asynchronous LLM decisions.
The market clearing process employs a dual-stage matching algorithm. In the first stage,
limit orders are posted. In the second stage, market orders are netted using a market-
to-market matching engine that processes buy and sell orders, reconciling orders based on
available agent cash and share commitments. In the third stage, any remaining market
orders are matched against the existing order book, with unfilled quantities converted to
aggressive limit orders. This three-tiered approach optimizes immediate execution and price
discovery while maintaining market liquidity.
The system’s OrderMatchingService orchestrates this process by coordinating trade ex-
ecutions through the TradeExecutionService and managing order state transitions via the
OrderStateManager. Each trade is logged in detail, with the overall market state—including
order books, market depth, and price evolution—recalculated at the end of each trading
round.
This modular design in the matching and clearing engine provides several advantages.
First, it enables rigorous trade validation where each market order is validated against agent
cash commitments and position constraints before matching, with the system dynamically
adjusting order quantities based on available cash when an agent’s commitment is insuf-
ficient, thus minimizing execution errors. Second, it offers flexible liquidity handling by
supporting market-to-market and market-to-book matching, ensuring orders have multiple
execution pathways, with unexecuted market orders converted to aggressive limit orders to
capture remaining liquidity. Third, it maintains detailed trade audit capabilities by recording
comprehensive traceability data including timestamps, trade volumes, executed prices, and
agent identifiers, thereby enabling post-trade analysis and performance benchmarking that
9
serves as the foundation for subsequent market efficiency and agent performance validations.
2.1.1 Market Mechanism Design
Our framework implements a continuous double-auction market mechanism that processes
orders in discrete trading rounds. We use discrete trading rounds because LLMs have latency
constraints, making it infeasible to process orders in real time. Within each round, the order
of agent submissions is randomized to avoid giving systematic priority to specific agents,
thus simulating concurrent order arrival while maintaining fairness. Once randomized, or-
ders are then processed according to standard price-time priority rules. The system supports
finite and infinite horizon markets, with differences in terminal conditions and wealth cal-
culation. In finite-horizon markets, agents are informed of the total number of rounds, and
their terminal wealth is calculated by redeeming all shares at the fundamental value of the
final round. In infinite-horizon markets, no terminal information is provided to agents, and
final wealth is determined using the last market price for share valuation. This design choice
enables researchers to study how time horizons influence trading strategies and price for-
mation, particularly how agents balance short-term trading opportunities against long-term
value considerations.
In a double auction, buyers and sellers actively submit orders, with trades occurring when
compatible buy and sell orders match the price. The matching engine processes these orders
through three sequential phases:
First, incoming limit orders that do not immediately cross the market are added to
the order book, maintaining strict price-time priority. Second, market orders are processed""",
            """2024). Another examines LLMs’ strategic capabilities through task-based simulations and
collaborative decision-making (Li, Zhang, and Sun 2023; Piatti et al. 2024).
Within the computer science literature, early works apply LLMs to financial markets but
abstract away many fundamental stock market characteristics. Often, they employ single-
price clearing mechanisms without a persistent order book, ignore partial fills and bid-ask
spreads, and omit dividends. Consequently, these simplified environments can primarily
address exogenous macro shocks (e.g., changes in interest rates or inflation; Gao et al. 2024),
exogenous policy changes (Zhang et al. 2024), or rely on advanced methods such as repetitive
next-token predictions to generate better answers (Koa et al. 2024). This work extends
these efforts by incorporating these crucial market features, enabling the study of complex
endogenous events such as flash crashes, liquidity shocks, and large-trader impacts.
This work also connects to emerging research on algorithmic and AI-powered trading
systems. Dou, Goldstein, and Ji (2024) demonstrate how reinforcement learning-based AI
speculators can autonomously learn to sustain collusive behavior without explicit coordi-
nation, achieving supra-competitive profits through either price-trigger strategies or self-
confirming bias in learning. This finding is particularly informative for this framework as
it highlights potential emergent behaviors that may arise when intelligent agents interact in
7
markets—behaviors that could manifest differently with LLM agents due to their natural
language reasoning capabilities. Similarly, Colliard, Foucault, and Lovo (2022) examine al-
gorithmic market makers using Q-learning and find they charge markups that increase when
adverse selection costs decrease—contrary to Nash equilibrium predictions. Their work pro-
vides methodological insights on how to test strategic pricing behaviors against theoretical
benchmarks incorporated into this LLM-based framework.
Finally, this approach is informed by complexity economics, which views markets as dy-
namic, non-equilibrium systems where agents adaptively learn and evolve strategies (Arthur
2013; Wolfram 2017). According to this view, markets exhibit emergent phenomena and
self-organization, especially when trading agents (human or artificial) update their behav-
ior in response to outcomes. This paradigm is particularly relevant in an era of increasing
automation and algorithmic trading (Balland et al. 2022; Ping 2019). Like adaptive agents
in complexity economics, these LLM traders incorporate new information and adjust their
strategies, generating emergent market patterns—a key motivation behind this framework.
Unlike previous frameworks that abstract away crucial market features or focus on narrow
strategies, this system incorporates realistic market microstructure while accommodating
heterogeneous agents interacting simultaneously. While earlier work demonstrates LLMs’
promise for macroeconomic modeling and simple trading simulations, this work introduces a
complex, open-source financial market platform that supports multiple agent architectures,
thorough market microstructure (limit orders, partial fills, dividends), and rigorous testing
protocols—fulfilling a critical need in complexity economics research and market microstruc-
ture analysis.
2 Methodology
The methodology section contains three parts. The first part describes the market design,
the second agents’ design, and the third the analysis module.
8
2.1 Market Design
Our methodological framework integrates three components that create a controlled envi-
ronment for LLM-based trading agents. The framework implements a flexible continuous
double-auction market mechanism that couples standard market microstructure principles
with market clearing and matching algorithms to accommodate asynchronous LLM decisions.""",
            """by detailed Trade Data, which records individual transaction details such as prices, quan-
tities, buyer and seller identifiers, timestamps, round information, and specific execution
details.
Agent Data provides insights into participant behavior by monitoring cash and share
25
Figure 5: Order Type Analysis under Systematic Variation. Displays the proportion of
Market vs. Limit orders used by different agent types across varying Price/Fundamental
ratios.
26
positions, portfolio values, wealth evolution, and agent type and strategy identifiers. Or-
der Data captures the complete lifecycle of trading decisions, including order specifications
(type, size, price), agent reasoning and justification, decision context and timing, and order
lifecycle events. Finally, Market State data maintains a comprehensive view of overall mar-
ket conditions through order book snapshots, market depth information, aggregate statistics,
and various market microstructure metrics.
2.3.3 Data Validation and Storage
The system implements a comprehensive set of data quality measures to ensure reliability and
consistency. The validation framework performs continuous checks for data completeness,
verifies consistency across related data streams, enforces format and type validation, and
maintains proper temporal sequencing of all recorded events. These validation mechanisms
work together to maintain data integrity throughout the experimental process.
The storage architecture employs multiple formats optimized for different data types and
use cases. Structured CSV files store tabular data for efficient analysis, while JSON formats
accommodate complex nested structures that preserve the rich relationships between market
elements. The system maintains detailed timestamped logs for debugging purposes and
generates summary statistics to facilitate quick analysis of experimental outcomes.
This comprehensive data collection architecture enables researchers to conduct detailed
analysis of market dynamics, validate agent behavior patterns, ensure experiment repro-
ducibility, and perform meaningful cross-experiment comparisons. The integrated approach
to data management provides the foundation for rigorous empirical investigation of market
behavior and agent interactions.
The framework implements specialized visualization techniques to analyze agent behavior
and market dynamics. Decision heatmaps plot agent actions across trading rounds, reveal-
ing strategic patterns and consistency. Trading flow visualizations track cumulative position
changes, identifying net buyers and sellers throughout market evolution. Reasoning word-
27
clouds extract key terms from agent explanations, providing insight into decision drivers
across different agent types.
The system also generates specialized market quality visualizations including bid-ask
spread evolution, price target accuracy, and agent valuation tracking. These visualizations
work in concert with the numerical metrics to provide both quantitative and qualitative
insights into agent behavior and market dynamics.
2.3.4 Validation Metrics and Performance Monitoring
The framework implements a comprehensive set of performance metrics and visualization
tools that monitor agent behavior and market dynamics. Market evolution visualizations
track price movements relative to fundamental values, including time series of transaction
prices, midpoint prices, and bid-ask spreads. These visualizations enable researchers to assess
market efficiency and price discovery processes throughout the simulation.
Agent performance metrics include absolute position tracking (shares, cash, and total
wealth), wealth composition analysis, position change metrics, and return calculations. The
system computes both absolute and percentage returns on various portfolio components
and compares performance across agent types to identify relative advantages of different""",
            """value, the system:
1. Sets market price P = ρV where ρ is the target ratio
2. Generates a consistent order book structure around this price
3. Executes multiple decision trials with the same agent type
4. Records decision outcomes (buy/sell/hold), order types, quantities, and reasoning
This process maps how LLM agents respond to different price environments, as illustrated
in Figures 2, 3, 4, and 5. The analysis reveals clear patterns in decision boundaries, with
distinct transitions between buying, selling, and holding regions that vary by agent type. For
example, value investors show strong buying tendencies when prices are below fundamental
value (ρ <1) and selling preferences when prices exceed fundamentals ( ρ >1). In contrast,
momentum traders show less sensitivity to the fundamental ratio and more responsiveness
to recent price trends.
The systematic variation approach also reveals patterns in order sizing and limit price
selection, with agents typically placing larger orders when prices deviate significantly from
their valuation models (Figure 4). This methodology provides unprecedented transparency
into LLM decision processes and enables quantitative comparison of different agent types
and LLM architectures.
22
Figure 2: Price Analysis under Systematic Variation. Shows how agent valuation estimates
and price targets respond to varying Price/Fundamental ratios.
The decision analysis can be customized for different experimental designs. For example,
researchers can use the framework to study the impact of various market conditions on agent
behavior by varying other market parameters or the effect of different agent types on market
dynamics by changing the agent population.
2.3 Data Collection and Analysis
Evaluating LLM trading agents requires robust methodologies for capturing, processing,
and analyzing their behavior in market environments. The framework implements a com-
prehensive analytics module that tracks all market activity, agent decisions, and performance
metrics throughout experimental runs. This multi-layered approach not only records what
happens in each simulation but also provides insights into why agents make specific deci-
sions, enabling researchers to validate agent behavior against their defined strategies and
assess overall market dynamics. The following sections detail the key components of this
analytics infrastructure.
23
Figure 3: Trading Decision Distribution under Systematic Variation. Illustrates the proba-
bility of Buy, Sell, or Hold decisions across different agent types as the Price/Fundamental
ratio changes.
24
Figure 4: Order Size Distribution under Systematic Variation. Shows the average quan-
tity traded (as a percentage of initial shares) for Buy and Sell orders across different
Price/Fundamental ratios.
2.3.1 Data Collection Architecture
The framework implements a comprehensive data collection system that captures multiple
dimensions of market behavior and agent decision-making. This structured approach ensures
reproducibility and enables detailed analysis of market dynamics.
2.3.2 Core Data Streams
The system captures five primary data streams that work together to provide a complete
picture of market activity. Market Data forms the foundation, tracking essential metrics
including price evolution, fundamental values, trading volumes, order book depth, market
liquidity, best bid/ask prices, spreads, and price-fundamental ratios. This is complemented
by detailed Trade Data, which records individual transaction details such as prices, quan-
tities, buyer and seller identifiers, timestamps, round information, and specific execution
details.
Agent Data provides insights into participant behavior by monitoring cash and share
25
Figure 5: Order Type Analysis under Systematic Variation. Displays the proportion of
Market vs. Limit orders used by different agent types across varying Price/Fundamental
ratios.
26""",
            """The theory of intermediation developed in Chapter 14 focuses on the risk-pooling and
risk-sharing products created by ﬁnancial-services institutions. Products examined
range from standardized instruments such as a group of mutual funds with charac-
teristics described in Theorem 15.5 to custom products tailored to meet the speciﬁc
requirements of each investor. Contingent-claims analysis (CCA) is the tool used
to derive the production technologies and costs for intermediaries to create these
custom derivative securities. As discussed, such ﬁnancial products and the associ-
ated activities of their producers are redundant in a frictionless environment with no
information-gathering or transactions costs. Thus, to provide a nontrivial role for
intermediaries in our equilibrium analysis here, we assume that some investors and
business ﬁrms face transactions costs for trading and issuing securities directly in
the capital markets. However, to preserve the CCA production theory for intermedi-
aries, we follow the model in Chapter 14 and posit that ﬁnancial intermediaries, as
the lowest-cost transactors, can trade continuously in the capital market at no cost.
2In this chapter, the returns on he growth-optimum portfolio are perfectly correlated with a combination of
themtraded securities used to hedge against state-variable changes. Hence, them m+ 2spanning funds of
Theorem 15.5 reduce to in m+ 1funds.
16.2 Financial Intermediation with Dynamically-Complete Markets 417
In applying this model to derive equilibrium prices and allocations, we shall further
assume that the ﬁnancial-services industry is competitive so that ﬁnancial-product
prices equal their marginal production costs.
In the production theory of Chapter 14, a manufacturing technology is developed
to create Arrow-Debreu securities that are contingent on traded asset prices. In this
section, we generalize that analysis to derive the production technology and cost
for intermediaries to create a complete set of Arrow-Debreu securities with payoffs
contingent on the state of the economy S(t)at each time t.
From (16.2), we can express ρijdt≡dqidqj,i,j= 1,. .. , n as functions of ρkiand
δij,k, i= 1,. . ., m andj=m+ 1,. .. , n . Deﬁne hjby
hj≡
fj−r−gjαj−r
σjj= 1,. . ., m
fj−r−gjm∑
i=1δijαi−r
σij=m+ 1,. .. , n(16.6)
LetΠ(S, t;S,τ)denote the solution to the linear partial differential equation
0 =1
2n∑
i=1n∑
j=1gigjρijSiSjΠij+n∑
j=1(r+hj)SjΠj+ Πt−rΠ (16.7)
subject to the boundary conditions that Π(S, t;S,τ)≥0and∫∞
0···∫∞
0Π(S, t;S,τ)dS1···dSn
exists for all Sandt < τ < ∞;Π(S, t;S,τ) =δ(S1−S1)δ(S2−S2)···δ(Sn−Sn)
where δ(·)is the Dirac delta function and S≡[S1,. . .,Sn]is a vector of speciﬁed pos-
itive numbers. Subscripts on Πdenote partial derivatives with respect to S1,. .. , S n,
andt.{hj,gj,r,ρij}are functions of Sandt, and under mild regularity conditions on
these functions, a solution to (16.7) exists and is unique.
Consider the continuous-trading portfolio strategy that allocates fraction
xj(t) =ΠjgjSj+∑n
k=m+1ΠkgkSkδjk
σjV(t)(16.8)
to traded asset j,j= 1,. .. , m and fraction 1−∑m
1xj(t)to the riskless security at
timet, where V(t)denotes the current value of the portfolio. It follows from (16.3),
(16.6), and (16.8) that the dynamics of the portfolio value can be written as
dV=V
m∑
j=1xj(αj−r) +r
dt+m∑
j=1xjσjdzj
=
rV+n∑
j=1ΠjSj(fj−hj−r)
dt+m∑
j=1(
ΠjgjSj+n∑
k=m+1ΠkgkSkδjk)
dzj
=
rV+n∑
j=1ΠjSj(fj−hj−r)
dt+n∑
j=1ΠjgjSjdqj
(16.9)
because, from (16.2), dqk=∑m
1δjkdqj,k=m+1,. . ., n , and, from (16.4), dzj=dqj,
j= 1,. .. , m .
418 A Complete-Markets General Equilibrium Theory of Finance in Continuous Time
Πis a solution to (16.7) and is therefore twice-continuously differentiable. Thus,
Itˆo’s lemma can be used to describe the stochastic process for Y(t)≡Π[S(t),t;S,τ]
as
dY=
1
2n∑
i=1n∑
j=1gigjρijSiSjΠij+n∑
j=1ΠjfjSj+ Πt
dt+n∑
j=1ΠjgjSjdqj(16.10)
where Πand its derivatives are evaluated at S=S(t)at each time t. Because Π""",
            """allocations are brieﬂy addressed in Chapter 15 and analyzed more fully in Chapter 16. If a set of existing
securities and markets leads to an equilibrium that is an unconstrained Pareto optimum, then any additional
securities or markets will be redundant.
50The term “transactions costs” can, of course, mean more than just the bid-ask spread or commissions
paid for buying and selling assets. For example, if an investor literally traded his portfolio continuously, he
would have no time to do anything else! Because investment management and ﬁnancial intermediation involve
primarily information processing and security trading, there arc signiﬁcant economies of scale. One would thus
expect substantially lower costs for the individual investor to use intermediaries instead of transacting directly
in the asset markets.
368 Financial Intermediation in the Continuous-Time Model
It would seem therefore that the same dichotomy derived in the frictionless-market
case applies also to our model with transactions costs. In a formal computational
sense it does. We can still solve for the equilibrium asset-price dynamics in the model
of Chapter 15 and then compute the prices of derivative securities, mutual funds, and
corporate liabilities using CCA. There is one signiﬁcant difference, however: the
ﬁrst-part calculation of equilibrium real-sector allocations is valid if and only if there
exists a sufﬁciently rich set of securities and intermediaries in the ﬁnancial sector to
make these allocations feasible for agents who cannot trade without cost. Because
of this conditioning. perhaps a more appropriate term for this separation is “quasi-
dichotomy.”
With the assumption that not all agents can trade continuously without cost, a
signiﬁcant economic role is established for derivative-security markets and ﬁnancial
intermediaries in the model. Somewhat paradoxically, we ﬁnd that, if intermediation
is efﬁcient, then derivative securities and the ﬁnancial products of the intermediaries
will be priced as if they are redundant.51Under these conditions, quasi-dichotomy
obtains, and we can derive equilibrium real-sector allocations and asset prices from
the frictionless-market version of the model.
14.6 Afterword: Policy and Strategy in Financial Intermediation
In this chapter, as throughout the book, the focus has been on theory. Allusions to
practice were concentrated on the micro quantitative applications of the continuous-
time model to product technologies and risk management. Still, I cannot wholly
resist the temptation to call attention to the model’s potential for addressing broader
issues in the practice of intermediation. And so this afterword shall ever so brieﬂy
touch upon implications of the model for intermediation policy and strategy in the
hope that it will lead others, better qualiﬁed, to explore this matter elsewhere.
Derivative securities have long been an integral part of the ﬁnancial markets,52
but most would mark the creation of the Chicago Board Options Exchange in April
1973 as the start of the current wave of ﬁnancial innovations involving derivative
securities. The succeeding years have witnessed an unprecedented proliferation of
organized trading markets in both equity and ﬁxed-income derivative instruments.
In turn, these markets made possible the creation of a wide range of ﬁnancial prod-
51Thus, our model provides a resolution to Hakansson’s (1979, p. 722) “The Catch 22 of Option Pricing.”
Although the equilibrium prices of options and other derivative securities satisfy the redundancy condition of
CCA, they are nevertheless needed to support the equilibrium allocations, and hence their elimination would
reduce social welfare.
52Bernstein (1992) reports that Aristotle’s anecdote about Thales in Book I of Politics is the ﬁrst recorded
mention of a ﬁnancial option. Schaede (1988) makes the case that the Dojima rice market in Osaka was a""",
            """market efficiency and price discovery processes throughout the simulation.
Agent performance metrics include absolute position tracking (shares, cash, and total
wealth), wealth composition analysis, position change metrics, and return calculations. The
system computes both absolute and percentage returns on various portfolio components
and compares performance across agent types to identify relative advantages of different
strategies. Trading flow analysis visualizes the volume of shares moving between different
agent types and cumulative net trading flows, revealing which agents act as net buyers or
sellers in different market conditions.
Decision pattern analysis employs heatmaps to visualize the consistency of agent decision-
making over time, allowing researchers to identify shifts in strategic behavior. This is com-
plemented by decision quantities visualization that plots order sizes to highlight variations
in trade aggressiveness across agent types. When agent reasoning data is available, the
system generates wordclouds to extract key terms from agent explanations, providing qual-
itative insights into decision drivers for different agent strategies. Additional visualizations
track price target accuracy and compare agent-specific valuations to realized market prices,
28
offering insights into the forecasting abilities of different agents.
A key advantage of simulation-based analysis is complete observability of all market
processes and agent states. Unlike real-world markets where data availability is often limited,
the framework captures every interaction, decision, and state change with perfect fidelity.
This comprehensive data collection allows researchers to compute additional metrics beyond
standard market measures, enabling novel analyses such as counterfactual testing (e.g., how
would markets evolve with different agent compositions), causal inference of specific agent
behaviors on market outcomes, and the development of custom efficiency or stability metrics
tailored to particular research questions. The system’s modular design facilitates rapid
implementation of new metrics and visualizations as research questions evolve.
3 Experimental Design and Results
Our experimental framework implements a dividend-paying asset market with heterogeneous
agents. The baseline simulation runs for 15 to 20 rounds with 8 participating agents, although
these parameters are fully configurable. Each agent begins with an initial endowment of
1,000,000 monetary units and 10,000 shares of the asset. The fundamental value of the asset
is set at $28.00, with a final redemption value matching this fundamental price in finite
horizon scenarios. Transaction costs are set to zero to isolate the effects of agent behavior
and market structure.
The dividend structure follows a stochastic process with a base payment of $1.40 and a
variation of ±$1.00, paid with 50% probability each round. This design creates uncertainty
in the asset’s income stream while maintaining a known expected value. Cash holdings earn
a risk-free interest rate of 5% per round, providing an opportunity cost for asset investment.
Agent composition is controlled through a flexible distribution system that allows for
various experimental configurations. In our baseline setup, we employ a mixed population
of value investors, momentum traders, and market makers. Each agent type implements
29
distinct trading strategies through Large Language Model (LLM) prompts, with GPT-4o as
the decision-making engine.
The data collection system captures comprehensive market activity across multiple di-
mensions. At the market level, it tracks the evolution of prices, fundamental values, and
realized dividends, providing insights into overall market dynamics. Individual agent data
includes detailed wealth trajectories and portfolio compositions, enabling analysis of strategy
effectiveness and wealth distribution patterns. The system maintains complete transaction""",
        ],
    ),
    LLMTestCase(
        input="Why do the authors choose discrete trading rounds instead of real‑time order processing for the LLM agents?",
        actual_output="""LLMs (Large Language Models, AI models that can understand and generate human-like text) have latency constraints (delays in processing information). This makes real-time order processing infeasible, so the authors use discrete trading rounds instead.""",
        expected_output="""LLMs have latency; discrete rounds let agents think while still approximating concurrency via randomised order of submission.""",
        context=[
            """When the market starts significantly above
the fundamental value (left panels), the price fails to converge downwards towards the $28.00
benchmark within the 15 rounds, remaining substantially elevated. Agent valuations mirror
this persistence, with many agents maintaining estimates well above the fundamental value.
However, when the market begins significantly below the fundamental value"""
        ],
        retrieval_context=[
            """the second agents’ design, and the third the analysis module.
8
2.1 Market Design
Our methodological framework integrates three components that create a controlled envi-
ronment for LLM-based trading agents. The framework implements a flexible continuous
double-auction market mechanism that couples standard market microstructure principles
with market clearing and matching algorithms to accommodate asynchronous LLM decisions.
The market clearing process employs a dual-stage matching algorithm. In the first stage,
limit orders are posted. In the second stage, market orders are netted using a market-
to-market matching engine that processes buy and sell orders, reconciling orders based on
available agent cash and share commitments. In the third stage, any remaining market
orders are matched against the existing order book, with unfilled quantities converted to
aggressive limit orders. This three-tiered approach optimizes immediate execution and price
discovery while maintaining market liquidity.
The system’s OrderMatchingService orchestrates this process by coordinating trade ex-
ecutions through the TradeExecutionService and managing order state transitions via the
OrderStateManager. Each trade is logged in detail, with the overall market state—including
order books, market depth, and price evolution—recalculated at the end of each trading
round.
This modular design in the matching and clearing engine provides several advantages.
First, it enables rigorous trade validation where each market order is validated against agent
cash commitments and position constraints before matching, with the system dynamically
adjusting order quantities based on available cash when an agent’s commitment is insuf-
ficient, thus minimizing execution errors. Second, it offers flexible liquidity handling by
supporting market-to-market and market-to-book matching, ensuring orders have multiple
execution pathways, with unexecuted market orders converted to aggressive limit orders to
capture remaining liquidity. Third, it maintains detailed trade audit capabilities by recording
comprehensive traceability data including timestamps, trade volumes, executed prices, and
agent identifiers, thereby enabling post-trade analysis and performance benchmarking that
9
serves as the foundation for subsequent market efficiency and agent performance validations.
2.1.1 Market Mechanism Design
Our framework implements a continuous double-auction market mechanism that processes
orders in discrete trading rounds. We use discrete trading rounds because LLMs have latency
constraints, making it infeasible to process orders in real time. Within each round, the order
of agent submissions is randomized to avoid giving systematic priority to specific agents,
thus simulating concurrent order arrival while maintaining fairness. Once randomized, or-
ders are then processed according to standard price-time priority rules. The system supports
finite and infinite horizon markets, with differences in terminal conditions and wealth cal-
culation. In finite-horizon markets, agents are informed of the total number of rounds, and
their terminal wealth is calculated by redeeming all shares at the fundamental value of the
final round. In infinite-horizon markets, no terminal information is provided to agents, and
final wealth is determined using the last market price for share valuation. This design choice
enables researchers to study how time horizons influence trading strategies and price for-
mation, particularly how agents balance short-term trading opportunities against long-term
value considerations.
In a double auction, buyers and sellers actively submit orders, with trades occurring when
compatible buy and sell orders match the price. The matching engine processes these orders
through three sequential phases:
First, incoming limit orders that do not immediately cross the market are added to
the order book, maintaining strict price-time priority. Second, market orders are processed""",
            """2024). Another examines LLMs’ strategic capabilities through task-based simulations and
collaborative decision-making (Li, Zhang, and Sun 2023; Piatti et al. 2024).
Within the computer science literature, early works apply LLMs to financial markets but
abstract away many fundamental stock market characteristics. Often, they employ single-
price clearing mechanisms without a persistent order book, ignore partial fills and bid-ask
spreads, and omit dividends. Consequently, these simplified environments can primarily
address exogenous macro shocks (e.g., changes in interest rates or inflation; Gao et al. 2024),
exogenous policy changes (Zhang et al. 2024), or rely on advanced methods such as repetitive
next-token predictions to generate better answers (Koa et al. 2024). This work extends
these efforts by incorporating these crucial market features, enabling the study of complex
endogenous events such as flash crashes, liquidity shocks, and large-trader impacts.
This work also connects to emerging research on algorithmic and AI-powered trading
systems. Dou, Goldstein, and Ji (2024) demonstrate how reinforcement learning-based AI
speculators can autonomously learn to sustain collusive behavior without explicit coordi-
nation, achieving supra-competitive profits through either price-trigger strategies or self-
confirming bias in learning. This finding is particularly informative for this framework as
it highlights potential emergent behaviors that may arise when intelligent agents interact in
7
markets—behaviors that could manifest differently with LLM agents due to their natural
language reasoning capabilities. Similarly, Colliard, Foucault, and Lovo (2022) examine al-
gorithmic market makers using Q-learning and find they charge markups that increase when
adverse selection costs decrease—contrary to Nash equilibrium predictions. Their work pro-
vides methodological insights on how to test strategic pricing behaviors against theoretical
benchmarks incorporated into this LLM-based framework.
Finally, this approach is informed by complexity economics, which views markets as dy-
namic, non-equilibrium systems where agents adaptively learn and evolve strategies (Arthur
2013; Wolfram 2017). According to this view, markets exhibit emergent phenomena and
self-organization, especially when trading agents (human or artificial) update their behav-
ior in response to outcomes. This paradigm is particularly relevant in an era of increasing
automation and algorithmic trading (Balland et al. 2022; Ping 2019). Like adaptive agents
in complexity economics, these LLM traders incorporate new information and adjust their
strategies, generating emergent market patterns—a key motivation behind this framework.
Unlike previous frameworks that abstract away crucial market features or focus on narrow
strategies, this system incorporates realistic market microstructure while accommodating
heterogeneous agents interacting simultaneously. While earlier work demonstrates LLMs’
promise for macroeconomic modeling and simple trading simulations, this work introduces a
complex, open-source financial market platform that supports multiple agent architectures,
thorough market microstructure (limit orders, partial fills, dividends), and rigorous testing
protocols—fulfilling a critical need in complexity economics research and market microstruc-
ture analysis.
2 Methodology
The methodology section contains three parts. The first part describes the market design,
the second agents’ design, and the third the analysis module.
8
2.1 Market Design
Our methodological framework integrates three components that create a controlled envi-
ronment for LLM-based trading agents. The framework implements a flexible continuous
double-auction market mechanism that couples standard market microstructure principles
with market clearing and matching algorithms to accommodate asynchronous LLM decisions.""",
            """(2023)). This work, however, focuses on financial markets and how LLM agents can operate
as full-fledged trading participants.
Recent research examines specific applications of LLMs for trading. FinMem and Trad-
ingGPT introduce frameworks with layered memory systems and customizable agent traits
5
to improve financial decision-making (Yu, Li, et al. 2024; Li, Zhang, and Sun 2023). Hierar-
chical multi-agent architectures have been explored in FinCon, which uses a manager-analyst
setup for collaborative portfolio decisions (Yu, Yao, et al. 2024). QuantAgent implements
a self-improving signal-mining approach (Wang et al. 2024), while other work underscores
the importance of long-term memory in LLM agents via vector databases (Hatalis et al.
2024). This line of research builds on successful reinforcement learning applications such as
AlphaPortfolio (Cong et al. 2021) and AlphaManager (Campello, Cong, and Zhou 2023),
which leverage deep RL and robust control for portfolio management.
Analyzing LLM agent behavior by changing only some parameters draws on methods
from the interpretable machine learning literature. In particular, the systematic variation
of market parameters to reveal decision patterns mirrors partial dependence plots and in-
dividual conditional expectation curves used to interpret complex machine learning models
(Molnar 2022). These techniques help reveal how LLM agents respond to changes in specific
variables while holding others constant, providing insight into their internal decision-making
processes that would otherwise remain opaque.
Beyond finance, studies of LLM capabilities in interactive or multi-agent settings offer
valuable insights. Benchmarks like AgentBench evaluate LLMs’ performance in interac-
tive tasks (Liu et al. 2023), while InvestorBench focuses on financial decision-making tasks
specifically (H. Li et al. 2024). NegotiationArena demonstrates LLMs’ capacity for strategic
interaction in bargaining contexts (Bianchi et al. 2024). Similarly, Guo et al. (2024) provide
an economics ”arena” where LLMs compete in strategic games, revealing that advanced
models like GPT-4 can exhibit rational, adaptive behavior—albeit not always reaching Nash
Equilibrium. Existing frameworks typically assess individual agents or hierarchical collab-
orations, whereas this work studies emergent market behaviors that arise from multiple
independent LLM traders interacting in a marketplace.
The approach also connects to the tradition of experimental asset markets. For instance,
Weitzel et al. (2020) show that even finance professionals are susceptible to speculative
6
bubbles, especially amid high capital inflows. Kop´ anyi-Peuker and Weber (2021) find that
trading experience alone does not eliminate bubbles, challenging assumptions about rational
market learning. Kirchler, Huber, and St¨ ockl (2012) identify confusion about fundamental
values as a key driver of bubble formation. This framework offers a new way to study these
phenomena with LLM traders, which can be rigorously parameterized for sophistication,
strategy, and information processing. Hence, this paper provides a method to investigate
how automated or ”artificial” agents might affect market stability or volatility.
Other recent work highlights the versatility of LLM agents in complex, interactive sce-
narios beyond finance. One stream focuses on simulating social behaviors—such as opinion
dynamics (Chuang et al. 2023), trust (Xie et al. 2024), and resource-sharing (Piatti et al.
2024). Another examines LLMs’ strategic capabilities through task-based simulations and
collaborative decision-making (Li, Zhang, and Sun 2023; Piatti et al. 2024).
Within the computer science literature, early works apply LLMs to financial markets but
abstract away many fundamental stock market characteristics. Often, they employ single-
price clearing mechanisms without a persistent order book, ignore partial fills and bid-ask""",
            """Can Large Language Models Trade? Testing Financial
Theories with LLM Agents in Market Simulations
Alejandro Lopez-Lira∗
First Version: November 29, 2024; Current Version: April 16, 2025
Abstract
This paper presents a realistic simulated stock market where large language models
(LLMs) act as heterogeneous competing trading agents. The open-source framework
incorporates a persistent order book with market and limit orders, partial fills, div-
idends, and equilibrium clearing alongside agents with varied strategies, information
sets, and endowments. Agents submit standardized decisions using structured outputs
and function calls while expressing their reasoning in natural language. Three findings
emerge: First, LLMs demonstrate consistent strategy adherence and can function as
value investors, momentum traders, or market makers per their instructions. Second,
market dynamics exhibit features of real financial markets, including price discovery,
bubbles, underreaction, and strategic liquidity provision. Third, the framework enables
analysis of LLMs’ responses to varying market conditions, similar to partial dependence
plots in machine-learning interpretability. The framework allows simulating financial
theories without closed-form solutions, creating experimental designs that would be
costly with human participants, and establishing how prompts can generate correlated
behaviors affecting market stability.
Keywords: LLM Agents; Agent-Based Markets; Experimental Finance; AI Trading;
Multi-Agent Systems
∗University of Florida. Email: alejandro.lopez-lira@warrington.ufl.edu. I am grateful to seminar par-
ticipants at the London Business School, Oxford University, Stockholm School of Economics, University of
Virginia, and the City University of Hong Kong for helpful suggestions and feedback.
1
arXiv:2504.10789v1  [q-fin.CP]  15 Apr 2025
1 Introduction
Large language models (LLMs) can increasingly function as autonomous agents—systems
that observe, reason, and act independently. LLMs have shown promising results in finan-
cial forecasting, but their potential as trading agents introduces a fundamental shift from
algorithms with explicit objectives to systems guided by natural language instructions. This
change raises critical questions: Can LLMs execute trading strategies? Do LLMs optimize
for profit maximization? What are the implications for market stability and efficiency?
If LLMs trade similarly to humans, they could enable experimental market simulations
without human participants. Conversely, if their trading behavior differs, understanding
these differences becomes critical for systemic risk management. These questions extend be-
yond theory; LLM-based strategies are already being deployed.1 To address these questions,
I develop an open-source simulation that tests LLM trading agents in a realistic market envi-
ronment with a persistent order book, supporting various order types, stochastic dividends,
and heterogeneous information.
The framework allows heterogeneous LLMs—defined in natural language, using different
system prompts—to act as diverse types of traders, such as value investors, momentum
traders, market makers, and contrarians. Agents submit standardized trading decisions in a
human-readable format while expressing their reasoning transparently. Figure 1 illustrates
this approach, showing how a speculator agent combines explicit valuation reasoning with
structured trading parameters, enabling systematic analysis and insight into the agent’s
decision-making process.
The analysis reveals three key findings about LLMs’ capabilities as trading agents. First,
LLMs can effectively execute trading strategies. They consistently understand market me-
chanics, process market information, form price expectations, and execute trades according
to specific instructions. Their trading behavior is highly sensitive to the prompts they
receive—they faithfully follow directions regardless of profit implications. This observance""",
            """decision-making process.
The analysis reveals three key findings about LLMs’ capabilities as trading agents. First,
LLMs can effectively execute trading strategies. They consistently understand market me-
chanics, process market information, form price expectations, and execute trades according
to specific instructions. Their trading behavior is highly sensitive to the prompts they
receive—they faithfully follow directions regardless of profit implications. This observance
1. For example, Autopilot has a ChatGPT-based portfolio https://x.com/thegptinvestor.
2
{"valuation_reasoning":
"The fundamental value is based on the expected dividend,
and the interest rate.
The expected dividend is $1.40, and the interest rate is 5%.
Using a perpetuity formula, the value is $1.40 / 0.05 = $28.",
"valuation":28.0,
"price_target_reasoning":"The current price is $29.00, which is
slightly above the fundamental value of $28.00. I expect the price
to remain around $29.00 in the next round due to market stability.",
"price_target":29.0,
"orders":[{"decision":"Sell","quantity":1000,"order_type":"limit",
"price_limit":29.50}],
"replace_decision":"Add",
"reasoning":"The current price is slightly above the fundamental value.
I will place a limit sell order at $29.50 to capitalize on potential price
increases."}
Figure 1: Example of a structured trading decision from a Speculator agent defined by its
system prompt: “You are a speculator who tries to profit from market inefficiencies.”. The
LLM provides explicit reasoning for its valuation, price target, and trading decision in a
machine-readable JSON format that can be directly processed by the trading system.
highlights a fundamental difference from human traders: LLMs do not inherently optimize
for profit maximization but rather for following instructions accurately.
Second, LLMs react meaningfully to market dynamics. They consider current and his-
torical prices, dividends, and other market information when making decisions. However,
they maintain their strategic direction even when market conditions change, following their
instructions even if doing so results in financial losses. This combination of responsiveness
to market conditions while maintaining strategic consistency creates a unique trading profile
distinct from rule-based algorithms and human traders.
Third, market dynamics with LLM agents can resemble actual markets and mirror classic
results from the theoretical finance literature. When these agents interact, they produce
realistic price discovery and liquidity provision with emergent behaviors, including price
convergence toward fundamental values. Depending on the distribution of agent types,
the system can generate various market phenomena, such as bubbles or underreactions to
information. This complex behavior suggests potential applications for studying market
3
dynamics using LLM agents instead of experiments with human participants.
Hence, these findings raise important questions about algorithmic consistency in LLM-
based systems. Since trading agents are implemented through prompts, their behavior in-
herits characteristics of the underlying language models. The standardization of LLM ar-
chitectures across implementations could create unexpected behavioral patterns—if many
agents are based on similar foundation models, they might exhibit correlated responses to
specific market conditions, potentially amplifying market instabilities.
To enable this analysis and accelerate development in this emerging field, we provide
an open-source framework with three key components: (1) a structured protocol for im-
plementing and validating LLM trading agents, supporting both LLM-based and traditional
rule-based agents; (2) a controlled market environment with realistic microstructure for test-
ing agent interactions; and (3) a comprehensive data collection system for analyzing trading
behavior. This framework serves multiple stakeholders in preparation for the evolution of""",
            """2407.18957. arXiv: 2407.18957 [q-fin]. http://arxiv.org/abs/2407.18957.
41
A Technical Implementation Details
A.1 Agent Type Specifications
This section details the base system prompts for each agent type in our simulation. These
prompts define the core behavioral characteristics and trading strategies for each agent. Each
prompt consists of:
• A role definition that establishes the agent’s trading philosophy
• A structured trading strategy that guides decision-making
• Specific instructions for when to use market orders vs limit orders
At runtime, these base prompts are combined with:
• Current market state (price, volume, order book depth)
• Position information (current holdings and available cash)
• Trading options and required response format
The standard runtime template includes:
Position Information Template
Your Position:
- Available Shares: {shares} shares (Short selling is not allowed)
- Main Cash Account: ${cash:.2f}
- Dividend Cash Account (not available for trading): ${dividend_cash:.2f}
- Total Available Cash: ${total_available_cash:.2f} (Borrowing is not allowed)
- Shares in Orders: {committed_shares} shares
- Cash in Orders: ${committed_cash:.2f}
42
Trading Options Template
Your analysis should include:
- valuation_reasoning: Your numerical analysis of the asset’s fundamental value
- valuation: Your estimate of the asset’s current fundamental value
- price_target_reasoning: Your numerical analysis of the asset’s price target
- price_target: Your predicted price for the next round
- reasoning: Your explanation for the trading decision
Trading Options:
1. New Orders (replace_decision=’Add’):
- Single or multiple orders allowed
- For each order:
- Market order: Set order_type=’market’
- Limit order: Set order_type=’limit’ and specify price_limit
- IMPORTANT: Sell orders require sufficient available shares
- Short selling is NOT allowed
2. Cancel Orders (replace_decision=’Cancel’):
- Return an empty orders list: orders=[]
Your decision must include:
- orders: list of orders (empty list for Hold/Cancel)
- For Buy/Sell orders, each must contain:
- decision: "Buy" or "Sell"
- quantity: number of shares
- order_type: "market" or "limit"
- price_limit: required for limit orders
- reasoning: brief explanation
- replace_decision: "Add", "Cancel", or "Replace"
43
Base System Prompts The following are the base system prompts for each LLM-based
agent type:
A.1.1 Value-Based Agents
Value Investor
You are a value investor who focuses on fundamental analysis.
You believe in mean reversion and try to buy undervalued assets and sell overvalued ones.
A.1.2 Trend-Following Agents
Momentum Trader
You are a momentum trader who focuses on price trends and volume.
You believe that ’the trend is your friend’ and try to identify and follow market momentum.
A.1.3 Liquidity Providers Agents
Market Maker
You are a professional market maker who provides liquidity to the market.
Your profit comes from capturing the spread between bid and ask prices, not from directional price movement.
IMPORTANT: There is NO SHORT SELLING allowed. You can only sell shares you already own.
Trading Guidelines:
- Place LIMIT buy orders slightly below the current market price (1-3% lower)
- Place LIMIT sell orders slightly above the current market price (1-3% higher)
- Your spread should be proportional to volatility but typically 2-6% of price
- NEVER place sell orders more than 10% above your buy orders
- Adjust your spread width based on recent price volatility
44
Inventory Management (No Short Selling):
- Monitor your current inventory in the market data
- Only place sell orders for quantities you actually own
- If you have no inventory, focus on buy orders first
- As you acquire inventory, gradually place sell orders
- If inventory grows too large, reduce or pause buy orders
- Adjust your buy/sell ratio based on current inventory level
Example: If price = $100, you might place buy orders at $97-99 and sell orders at $101-103,""",
            """• Market Makers: Provide liquidity through symmetric bid-ask spreads
• Contrarian Traders: Trade against market extremes and overreactions
• Speculators: Seek to profit from market inefficiencies
• Sentiment-Based Agents: Include optimistic and pessimistic variants with biased
expectations
• Retail Traders: Simulate typical individual investor behavior
The software also includes a set of deterministic rule-based agents that serve as bench-
marks and control conditions:
• Directional Traders: Always-buy, always-sell, and always-hold agents
• Technical Agents: Gap traders, mean reversion traders, and momentum traders
• Algorithmic Market Makers: Implement fixed spread-posting strategies
14
Each agent type is defined by its system prompt (for LLM agents) or algorithmic rules (for
deterministic agents), with standardized interfaces enabling direct comparison across diverse
strategies. The agent composition system supports flexible specifications—including uni-
form distributions, type-specific concentrations (e.g., ”value heavy”), and precise numerical
allocations—enabling systematic exploration of how market dynamics emerge from different
agent populations.
The framework’s extensible design makes it remarkably simple to add new agent types—
LLM-based agents require only defining a new system prompt that specifies the trading
strategy. In contrast, deterministic agents can be implemented through the standard agent
interface. This flexibility allows researchers to rapidly prototype and deploy novel trading
strategies without modifying the underlying system architecture.
The complete list of agent types included in the framework and their detailed specifi-
cations is provided in the Appendix. The framework’s flexible prompt-based architecture
allows researchers to rapidly prototype and deploy new agent types by developing appropri-
ate strategic and tactical prompts without modifying the underlying system architecture.
2.2.4 User Prompt
The user prompt provides the immediate market context necessary for tactical decision-
making. This dynamic component delivers current market state information, including
prices, volumes, and emerging trends, alongside the agent’s current position information
and available trading options. Additionally, the user prompt specifies immediate decision
requirements and operational constraints, ensuring that agent responses remain within fea-
sible bounds while aligning with their strategic objectives. This separation of strategic and
tactical prompting enables precise control over agent behavior while maintaining flexibility
for market interactions. All the information in the user prompt is optional at the agent level
and can be customized for different experimental designs.
15
2.2.5 Decision Structure
Each agent decision follows a standardized output format comprising several key components.
The decision field specifies the basic action as either Buy, Sell, or Hold. For active trades,
the quantity field determines the number of shares to trade, while the order type indicates
whether it is a Market or Limit order. When placing limit orders, the price limit field
specifies the maximum (for buys) or minimum (for sells) acceptable execution price. Finally,
each decision includes a reasoning field that provides an explicit rationale for the trading
decision, ensuring transparency and facilitating analysis of agent behavior.
2.2.6 Structured Outputs and Function Calling
Our framework implements a structured output approach using function calling to ensure
standardized, human-readable, machine-readable agent decisions. This technique allows
LLMs to generate outputs in a specific format that can be directly validated and processed
by the trading system, bridging the gap between natural language reasoning and executable
trading actions.
The system uses Pydantic for validation and parsing of agent outputs, with a schema-
based approach that defines the required structure:
class TradeDecisionSchema(BaseModel):""",
            """ceedings of the 62nd Annual Meeting of the Association for Computational Linguistics
(Volume 1: Long Papers),edited by Lun-Wei Ku, Andre Martins, and Vivek Srikumar,
15523–15536. ACL 2024. Bangkok, Thailand: Association for Computational Linguis-
tics, August.
39
Li, Yuan, Yixuan Zhang, and Lichao Sun. 2023. “MetaAgents: Simulating Interactions of
Human Behaviors for LLM-based T Ask-Oriented Coordination via Collaborative Gen-
erative Agents.” arXiv.org.
Liu, Xiao, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, et al. 2023.
“AgentBench: Evaluating LLMs as Agents.”International Conference on Learning Rep-
resentations.
Lopez-Lira, Alejandro, and Yuehua Tang. 2023. “Can ChatGPT Forecast Stock Price Move-
ments? Return Predictability and Large Language Models.” SSRN Electronic Journal
(April 6, 2023).
Manning, Benjamin S., Kehang Zhu, and John J. Horton. 2024. “Automated Social Science:
Language Models as Scientist and Subjects.” (Cambridge, MA) (April 29, 2024).
Molnar, Christoph. 2022. Interpretable Machine Learning.
Pelster, Matthias, and Joel Val. 2023. “Can Chatgpt Assist in Picking Stocks?”Social Science
Research Network.
Piatti, Giorgio, Zhijing Jin, Max Kleiman-Weiner, Bernhard Sch¨ olkopf, Mrinmaya Sachan,
and Rada Mihalcea. 2024. “Cooperate or Collapse: Emergence of Sustainable Coopera-
tion in a Socie Ty of LLM Agents.” arXiv.org.
Ping, Chen. 2019. “From Complexity Science to Complexity Economics.” In Alternative
Approaches to Economic Theory,19–55. Routledge, June 11, 2019.
Wang, Saizhuo, Hang Yuan, Lionel M. Ni, and Jian Guo. 2024. “QuantAgent: Seeking Holy
Grail in Trading by Self-Improving Large Lang Uage Model.” arXiv.org.
Weitzel, Utz, Christoph Huber, J¨ urgen Huber, Michael Kirchler, Florian Lindner, and Julia
Rose. 2020. “Bubbles and Financial Professionals.” The Review of Financial Studies33,
no. 6 (June 1, 2020): 2659–2696.
40
Wolfram, Elsner. 2017. “Complexity Economics as Heterodoxy: Theory and Policy.”Journal
of Economic Issues51, no. 4 (October 2, 2017): 939–978.
Woodhouse, Drew, and Alex Charlesworth. 2023. “Can ChatGPT Predict Future Interest
Rate Decisions?” Social Science Research Network.
Xie, Chengxing, Canyu Chen, Feiran Jia, Ziyu Ye, Shiyang Lai, Kai Shu, Jindong Gu, et al.
2024. “Can Large Language Model Agents Simulate Human Trust Behavior?”arXiv.org.
Yang, Stephen. 2023. “Predictive Patentomics: Forecasting Innovation Success and Valuation
w Ith ChatGPT.” Social Science Research Network.
Yu, Yangyang, Haohang Li, Zhi Chen, Yuechen Jiang, Yang Li, Denghui Zhang, Rong
Liu, Jordan W. Suchow, and Khaldoun Khashanah. 2024. “FinMem: A Performance-
Enhanced LLM Trading Agent with Layered Memory a Nd Character Design.”Proceed-
ings of the AAAI Symposium Series3, no. 1 (May 20, 2024): 595–597.
Yu, Yangyang, Zhiyuan Yao, Haohang Li, Zhiyang Deng, Yupeng Cao, Zhi Chen, Jordan W.
Suchow, et al. 2024. “FinCon: A Synthesized LLM Multi-Agent System with Conceptual
Verbal Reinforcement for Enhanced Financial Decision Making.” Pre-published, Novem-
ber 7, 2024. Accessed January 8, 2025. https://doi.org/10.48550/arXiv.2407.06567.
arXiv: 2407.06567 [cs]. http://arxiv.org/abs/2407.06567.
Zhang, Chong, Xinyi Liu, Zhongmou Zhang, Mingyu Jin, Lingyao Li, Zhenting Wang,
Wenyue Hua, et al. 2024. “When AI Meets Finance (StockAgent): Large Language
Model-based Stock Trading in Simulated Real-world Environments.” Pre-published,
September 21, 2024. Accessed January 26, 2025. https://doi.org /10.48550/arXiv .
2407.18957. arXiv: 2407.18957 [q-fin]. http://arxiv.org/abs/2407.18957.
41
A Technical Implementation Details
A.1 Agent Type Specifications
This section details the base system prompts for each agent type in our simulation. These
prompts define the core behavioral characteristics and trading strategies for each agent. Each
prompt consists of:
• A role definition that establishes the agent’s trading philosophy
• A structured trading strategy that guides decision-making""",
        ],
    ),
    LLMTestCase(
        input="What is the main experimental finding when the simulated market starts 25 % above the fundamental value?",
        actual_output="""In the infinite horizon scenario where the simulated market began 25% above the fundamental value (overvalued at $56.00 compared to the true value of $28.00), the price failed to converge downwards towards the fundamental value within the 15 trading rounds. The LLM (Large Language Model)-driven agents' valuations also remained significantly elevated above the fundamental value, mirroring the overall market's persistent overvaluation. This suggests that, under these specific conditions, the AI agents were less effective at correcting overvaluation compared to undervaluation within the given timeframe.""",
        expected_output="""With an initial price 25 % above fundamentals, prices failed to converge downward within 15 rounds and agents kept over‑valuing the asset.""",
        context=[
            """When the market starts significantly above the fundamental value … the price fails to converge downwards … remaining substantially elevated. Agent valuations mirror this persistence, with many agents maintaining estimates well above the fundamental value."""
        ],
        retrieval_context=[
            """bids/asks), and two Speculator agents (opportunistic traders seeking inefficiencies). Market
31
makers are given enhanced liquidity with 20x the baseline cash and shares to ensure suffi-
cient liquidity provision and facilitate price discovery. The scenario tests whether prices can
correct downward through trading activity when starting from an overvalued state.
3.2.2 Price Discovery (Below Fundamental)
This complementary scenario tests upward price convergence by starting with an initial price
25% below the fundamental value ( $21.00). It employs the identical agent composition and
parameters as the above-fundamental scenario, allowing for direct comparison of market
behavior under opposite initial mispricing conditions. This design enables researchers to
assess potential asymmetries in price discovery processes.
3.2.3 Infinite Horizon Price Discovery
We extend both price discovery scenarios to infinite horizon settings, where shares are not
redeemed at a terminal date. The initial prices are set at double ($56.00) and half ($14.00) the
fundamental value for the above and below fundamental scenarios respectively, creating more
extreme mispricing conditions. These scenarios run for 15 trading rounds and test whether
agents correctly value assets based on expected dividend streams rather than redemption
values. Each infinite horizon scenario involves two Default investors, two Optimistic traders,
two Market makers, and two Speculator agents.
The results from these infinite horizon scenarios reveal interesting asymmetries in price
discovery, as illustrated in Figure 6 and Figure 7. When the market starts significantly above
the fundamental value (left panels), the price fails to converge downwards towards the$28.00
benchmark within the 15 rounds, remaining substantially elevated. Agent valuations mirror
this persistence, with many agents maintaining estimates well above the fundamental value.
However, when the market begins significantly below the fundamental value (right panels),
the price exhibits a clear convergence towards the fundamental benchmark. Agent valuations
in this scenario also tend to adjust upwards, aligning more closely with the calculated fun-
32
damental value over time. This suggests that under these conditions, LLM agents are more
effective at correcting undervaluation than overvaluation within the simulated timeframe.
Figure 6: Price Evolution: Infinite Horizon Scenarios. Left: Initial price $56.00 (Above
Fundamental). Right: Initial price $14.00 (Below Fundamental). The dashed line indicates
the fundamental value ($28.00).
Figure 7: Agent Valuations: Infinite Horizon Scenarios. Left: Initial price $56.00 (Above
Fundamental). Right: Initial price $14.00 (Below Fundamental). Shows individual agent
estimates of fundamental value over time.
3.2.4 Divergent Beliefs
This scenario explores the impact of heterogeneous beliefs about fundamental value by com-
bining agents with systematically different valuation models. The agent composition is
designed to create heterogeneity: two Optimistic traders (believing the fundamental value is
significantly higher), two Pessimistic traders (believing it is significantly lower), two neutral
Market makers, two Momentum traders (following price trends rather than fundamentals),
and two Default investors (baseline agents). We test both above-fundamental (initial price
$56.00, 2x fundamental) and below-fundamental (initial price$14.00, 0.5x fundamental) vari-
33
ants, allowing researchers to study how different belief structures influence price formation
and trading patterns under different initial mispricings. In these scenarios, the fundamental
price is hidden from agents, forcing them to rely on their own valuation models.
3.2.5 Market Stress
This scenario tests market resilience under challenging conditions by creating a more volatile
environment. The scenario includes two consistently bullish Optimistic traders, two consis-""",
            """the decision-making engine.
The data collection system captures comprehensive market activity across multiple di-
mensions. At the market level, it tracks the evolution of prices, fundamental values, and
realized dividends, providing insights into overall market dynamics. Individual agent data
includes detailed wealth trajectories and portfolio compositions, enabling analysis of strategy
effectiveness and wealth distribution patterns. The system maintains complete transaction
records with prices, quantities, and counterparty information, facilitating the study of trad-
ing patterns and market microstructure. Additionally, it captures agent decision rationales
and strategy adherence metrics, allowing researchers to evaluate the consistency and effec-
tiveness of different trading approaches.
All experimental parameters, market outcomes, and agent interactions are systemati-
cally logged and stored in structured formats (CSV and JSON) for subsequent analysis. The
framework generates standardized visualizations of price evolution, wealth distribution, and
dividend payments to facilitate comparative analysis across different experimental configu-
rations.
3.1 Fundamental Value Calibration
The framework implements a consistent approach to fundamental value calculation that pro-
vides a reliable benchmark for price discovery. For infinite horizon markets, the fundamental
value follows the standard dividend discount model:
Vt = E[D]
r = Expected Dividend
Interest Rate (1)
For the default parameters where the expected dividend is $1.40 and the interest rate is
5%, this yields a fundamental value of $28.00.
In finite horizon markets with T periods remaining, the fundamental value incorporates
30
both future dividends and terminal redemption value K:
FVt =
TX
τ=t
E[D]
(1 + r)τ−t+1 + K
(1 + r)T−t+1 (2)
To ensure consistency between finite and infinite horizon markets, the redemption value
K is set equal to E[D]
r , which makes the fundamental value constant atE[D]
r across all periods,
regardless of the time horizon. This calibration approach ensures a clean experimental design
by providing a stable benchmark for price discovery.
3.2 Experimental Scenarios
To evaluate market dynamics with LLM-based agents, we implemented several experimental
scenarios that systematically explore different initial conditions and agent compositions.
Each scenario maintains the fundamental value of $28.00 while varying starting prices, time
horizons, and agent populations. These scenarios address our core research questions (Section
1) by testing LLM capabilities under varying market conditions, focusing on price discovery
dynamics, the impact of heterogeneous beliefs, and market stability under stress; GPT-4o
was used consistently as the decision-making engine for all LLM agents across these scenarios.
We present the setup for several key scenarios below, followed by a discussion of the observed
results for the 2 experiments involving an infinite horizon market with a starting price either
above or below the fundamental value.
3.2.1 Price Discovery (Above Fundamental)
This scenario tests downward price convergence by starting with an initial price 25% above
the fundamental value ( $35.00). It runs for 20 trading rounds and features a diverse
agent population, including two Default investors (baseline agents), two Optimistic traders
(who believe prices should be higher), two Market makers (providing liquidity by posting
bids/asks), and two Speculator agents (opportunistic traders seeking inefficiencies). Market
31
makers are given enhanced liquidity with 20x the baseline cash and shares to ensure suffi-
cient liquidity provision and facilitate price discovery. The scenario tests whether prices can
correct downward through trading activity when starting from an overvalued state.
3.2.2 Price Discovery (Below Fundamental)
This complementary scenario tests upward price convergence by starting with an initial price""",
            """33
ants, allowing researchers to study how different belief structures influence price formation
and trading patterns under different initial mispricings. In these scenarios, the fundamental
price is hidden from agents, forcing them to rely on their own valuation models.
3.2.5 Market Stress
This scenario tests market resilience under challenging conditions by creating a more volatile
environment. The scenario includes two consistently bullish Optimistic traders, two consis-
tently bearish Pessimistic traders, two Market makers (liquidity providers), and two Value
investors (rational benchmark traders). The scenario runs for 100 rounds to study long-term
market behavior and includes unequal initial endowments, with optimistic traders having
more cash (1.5x baseline) but fewer shares (0.5x baseline) and pessimistic traders having less
cash (0.5x baseline) but more shares (1.5x baseline). This resource imbalance tests whether
particular agent types can dominate market outcomes through resource advantages.
The scenarios presented here demonstrate the framework’s capabilities for exploring di-
verse market conditions. Its modular structure facilitates the straightforward definition and
implementation of alternative experimental designs, enabling researchers to tailor simulations
to specific research questions.
In all scenarios, we maintain consistent baseline parameters with a fundamental value
of $28.00, calculated from the expected dividend of $1.40 and interest rate of 5%. Agent
endowments start at 1,000,000 monetary units and 10,000 shares unless specifically modified.
Transaction costs are set to zero to isolate the effects of agent behavior and market structure
on price formation.
4 Conclusion
This paper demonstrates that Large Language Models can effectively function as diverse
trading agents—from value investors to market makers—maintaining strategic consistency
34
while adapting to market conditions. Our experimental framework reveals that their in-
teractions generate realistic market dynamics, including phenomena like price bubbles and
corrections, highlighting both the capabilities and potential risks of deploying LLM agents
in financial markets.
These findings carry significant implications for market structure and regulation. While
LLM agents can enhance price discovery and liquidity, their adherence to programmed strate-
gies, even potentially flawed ones derived from prompts, could amplify market volatility or
introduce novel systemic risks, as observed in our simulated bubble scenarios. A key concern
is the potential for widespread correlated behavior: similar underlying LLM architectures
responding uniformly to comparable prompts or market signals could inadvertently create
destabilizing trading patterns without explicit coordination. This underscores the critical
need for rigorous testing and validation of LLM-based trading systems prior to live deploy-
ment.
A central contribution of this work is the open-source simulation framework itself, de-
signed to catalyze research into LLM trading agents. We invite the research community to
utilize and extend this platform to investigate pressing questions in this rapidly evolving
area. The framework enables systematic exploration of complex scenarios—such as hybrid
human-LLM markets, stress tests, varying market structures, regulatory impacts, and the
nuances of LLM prompting—often difficult or costly to study otherwise. Specific avenues
ripe for investigation using this tool include the emergence of novel trading strategies, the
precise effects of agent heterogeneity on market stability, and the development of robust
validation protocols for AI traders. As artificial intelligence becomes more integrated into
finance, collaborative research leveraging adaptable simulation environments like this one
will be crucial for understanding and responsibly shaping the future of trading.
35
References""",
            """market efficiency and price discovery processes throughout the simulation.
Agent performance metrics include absolute position tracking (shares, cash, and total
wealth), wealth composition analysis, position change metrics, and return calculations. The
system computes both absolute and percentage returns on various portfolio components
and compares performance across agent types to identify relative advantages of different
strategies. Trading flow analysis visualizes the volume of shares moving between different
agent types and cumulative net trading flows, revealing which agents act as net buyers or
sellers in different market conditions.
Decision pattern analysis employs heatmaps to visualize the consistency of agent decision-
making over time, allowing researchers to identify shifts in strategic behavior. This is com-
plemented by decision quantities visualization that plots order sizes to highlight variations
in trade aggressiveness across agent types. When agent reasoning data is available, the
system generates wordclouds to extract key terms from agent explanations, providing qual-
itative insights into decision drivers for different agent strategies. Additional visualizations
track price target accuracy and compare agent-specific valuations to realized market prices,
28
offering insights into the forecasting abilities of different agents.
A key advantage of simulation-based analysis is complete observability of all market
processes and agent states. Unlike real-world markets where data availability is often limited,
the framework captures every interaction, decision, and state change with perfect fidelity.
This comprehensive data collection allows researchers to compute additional metrics beyond
standard market measures, enabling novel analyses such as counterfactual testing (e.g., how
would markets evolve with different agent compositions), causal inference of specific agent
behaviors on market outcomes, and the development of custom efficiency or stability metrics
tailored to particular research questions. The system’s modular design facilitates rapid
implementation of new metrics and visualizations as research questions evolve.
3 Experimental Design and Results
Our experimental framework implements a dividend-paying asset market with heterogeneous
agents. The baseline simulation runs for 15 to 20 rounds with 8 participating agents, although
these parameters are fully configurable. Each agent begins with an initial endowment of
1,000,000 monetary units and 10,000 shares of the asset. The fundamental value of the asset
is set at $28.00, with a final redemption value matching this fundamental price in finite
horizon scenarios. Transaction costs are set to zero to isolate the effects of agent behavior
and market structure.
The dividend structure follows a stochastic process with a base payment of $1.40 and a
variation of ±$1.00, paid with 50% probability each round. This design creates uncertainty
in the asset’s income stream while maintaining a known expected value. Cash holdings earn
a risk-free interest rate of 5% per round, providing an opportunity cost for asset investment.
Agent composition is controlled through a flexible distribution system that allows for
various experimental configurations. In our baseline setup, we employ a mixed population
of value investors, momentum traders, and market makers. Each agent type implements
29
distinct trading strategies through Large Language Model (LLM) prompts, with GPT-4o as
the decision-making engine.
The data collection system captures comprehensive market activity across multiple di-
mensions. At the market level, it tracks the evolution of prices, fundamental values, and
realized dividends, providing insights into overall market dynamics. Individual agent data
includes detailed wealth trajectories and portfolio compositions, enabling analysis of strategy
effectiveness and wealth distribution patterns. The system maintains complete transaction""",
            """value, the system:
1. Sets market price P = ρV where ρ is the target ratio
2. Generates a consistent order book structure around this price
3. Executes multiple decision trials with the same agent type
4. Records decision outcomes (buy/sell/hold), order types, quantities, and reasoning
This process maps how LLM agents respond to different price environments, as illustrated
in Figures 2, 3, 4, and 5. The analysis reveals clear patterns in decision boundaries, with
distinct transitions between buying, selling, and holding regions that vary by agent type. For
example, value investors show strong buying tendencies when prices are below fundamental
value (ρ <1) and selling preferences when prices exceed fundamentals ( ρ >1). In contrast,
momentum traders show less sensitivity to the fundamental ratio and more responsiveness
to recent price trends.
The systematic variation approach also reveals patterns in order sizing and limit price
selection, with agents typically placing larger orders when prices deviate significantly from
their valuation models (Figure 4). This methodology provides unprecedented transparency
into LLM decision processes and enables quantitative comparison of different agent types
and LLM architectures.
22
Figure 2: Price Analysis under Systematic Variation. Shows how agent valuation estimates
and price targets respond to varying Price/Fundamental ratios.
The decision analysis can be customized for different experimental designs. For example,
researchers can use the framework to study the impact of various market conditions on agent
behavior by varying other market parameters or the effect of different agent types on market
dynamics by changing the agent population.
2.3 Data Collection and Analysis
Evaluating LLM trading agents requires robust methodologies for capturing, processing,
and analyzing their behavior in market environments. The framework implements a com-
prehensive analytics module that tracks all market activity, agent decisions, and performance
metrics throughout experimental runs. This multi-layered approach not only records what
happens in each simulation but also provides insights into why agents make specific deci-
sions, enabling researchers to validate agent behavior against their defined strategies and
assess overall market dynamics. The following sections detail the key components of this
analytics infrastructure.
23
Figure 3: Trading Decision Distribution under Systematic Variation. Illustrates the proba-
bility of Buy, Sell, or Hold decisions across different agent types as the Price/Fundamental
ratio changes.
24
Figure 4: Order Size Distribution under Systematic Variation. Shows the average quan-
tity traded (as a percentage of initial shares) for Buy and Sell orders across different
Price/Fundamental ratios.
2.3.1 Data Collection Architecture
The framework implements a comprehensive data collection system that captures multiple
dimensions of market behavior and agent decision-making. This structured approach ensures
reproducibility and enables detailed analysis of market dynamics.
2.3.2 Core Data Streams
The system captures five primary data streams that work together to provide a complete
picture of market activity. Market Data forms the foundation, tracking essential metrics
including price evolution, fundamental values, trading volumes, order book depth, market
liquidity, best bid/ask prices, spreads, and price-fundamental ratios. This is complemented
by detailed Trade Data, which records individual transaction details such as prices, quan-
tities, buyer and seller identifiers, timestamps, round information, and specific execution
details.
Agent Data provides insights into participant behavior by monitoring cash and share
25
Figure 5: Order Type Analysis under Systematic Variation. Displays the proportion of
Market vs. Limit orders used by different agent types across varying Price/Fundamental
ratios.
26""",
            """tory equilibrium theory of allocations and prices in the presence of transactions costs
promises still more complexity, because it requires a simultaneous endogenous de-
termination of prices, allocations, and the least-cost form of market structure and
ﬁnancial intermediation.
To circumvent all this complexity and also preserve a role for intermediation, I in-
troduce a continuous-time model in which many investors cannot trade costlessly, but
the lowest-cost transactors (by deﬁnition, ﬁnancial intermediaries) can. In this model,
standard CCA can be used to determine the production costs for ﬁnancial products is-
sued by intermediaries. However, unlike in the standard zero-cost model, these prod-
ucts can signiﬁcantly improve economic efﬁciency. If, moreover, the traded-security
markets and ﬁnancial-services industry are competitive, then equilibrium prices of
ﬁnancial products will equal the production costs of the lowest-cost transactors. In
Section 14.5, we analyze this model and show that, through intermediation, all in-
vestors can achieve optimal consumption-bequest allocations as if they could trade
continuously without cost. Hence, in this model with transactions costs, both the
contingent-claims analyzes of Chapters 11-13 and the equilibrium analyzes of Chap-
ter 15 can be used to determine equilibrium allocations and prices.4Thus, this model
provides a resolution of the Hakansson paradox by showing that mutual funds and
derivative-security markets can provide important economic beneﬁts to investors and
corporate issuers, even though these securities are priced in equilibrium as if they
were redundant.
3With diffusion processes and proportional transactions costs, investors cannot trade continuously, and
therefore cannot perfectly hedge derivative-security positions. The reason is that, with continuous trading,
transactions costs at each trade will be proportional to |dz|, where dzis a Brownian motion. However, for any
noninﬁnitesimal time interval T,∫T
0|dz|=∞almost certainly, and hence with continuous trading the total
transactions cost is unbounded with probability one.
4More generally, standard CCA will provide a close approximation if the “mark-up” per unit required
to cover the intermediary’s transactions costs and proﬁt is sufﬁciently small that, from the perspective of its
customers’ behavior, the additional cost is negligible. Of course, a tiny margin applied to large volume can
produce substantial total proﬁts for the ﬁnancial intermediation industry.
14.2 Derivative-Security Pricing with Transactions Costs 341
14.2 Derivative-Security Pricing with Transactions Costs
In this section, we examine the effects of transactions costs on derivative security
pricing by using the two-period version of the Cox-Ross-Rubinstein binomial option
pricing model as analyzed in Section 10.2. In that model, the initial stock price S(0)
is given by S0. At time 1, the stock price will equal either S11orS12. IfS(1) = S11,
then at time 2, S(2)will equal either S21orS22. IfS(1) = S12, then at time 2, S(2)
will equal either S23orS24.Rdenotes the return per dollar invested in the riskless
security and is constant over both periods. To capture the effect of transactions costs,
we assume that a commission must be paid on each purchase or sale of the stock
and that the commission rate is a ﬁxed proportion τof the dollar amount of the
transaction. Equivalently, we could assume a bid-ask spread, in which investors pay
theask price for the stock, Sa(t)≡(1 +τ)S(t), when they buy and receive the bid
price ,Sb(t)≡(1−τ)S(t)when they sell. There are no costs for transacting in the
riskless security.
As shown in (10.3), the array of possible stock prices must satisfy certain condi-
tions to rule out the possibility of arbitrage or dominance opportunities between the
stock and the riskless security. The corresponding set of restrictions, in the presence
of transactions costs can be written as
S11< S0R <(1−τ)S12
1 +τ(14.1a)
S21< S11R <(1−τ)S22""",
            """investors’ optimal demand functions will depend upon how frequently they can revise
their portfolios. Therefore, it should be pointed out that nowhere in the analysis
presented here is it assumed that the distribution of X(T)−X(0)is invariant to h.
Deﬁne the conditional expectation operator Etto be the expectation operator con-
ditional on knowing all relevant information revealed as of time tor before. Deﬁne
the random variables ǫ(k)by
ǫ(k)≡X(k)−X(k−1)−Ek−1{
X(k)−X(k−1)}
k= 1,. .. , n (3.2)
where “time k” is used as shorthand for “time kh.” By construction, Ek−1{ǫ(k)}= 0,
andǫ(k)is the unanticipated price change in the security between k−1andk, condi-
5See Merton (1975b).
3.1 Introduction 49
tional on being at time k−1. Moreover, by the properties of conditional expectation,
it follows that Ek−j{ǫ(k)}= 0forj= 1,. . ., k . Hence the partial sums Sn≡∑n
1ǫ(k)
form a martingale .6As will be seen, the mathematical analysis to follow depends
heavily on the properties of martingales. The theory of martingales is usually associ-
ated in the ﬁnancial economics literature with the “Efﬁcient-Market Hypothesis” of
Fama and Samuelson.7Therefore, the reader may be tempted to connect the martin-
gale property of the unanticipated returns derived here with an implicit assumption
that “securities are priced correctly.” However, the martingale property of the unan-
ticipated returns here is purely a result of construction, and therefore imposes no such
economics assumption. However, two economics assumptions that will be imposed
are as follows.
Assumption 5.
For each ﬁnite time interval [0,T]there exists a number A1>0, independent of the
number of trading intervals n, such that Var(Sn)≥A1where Var(Sn)≡E0{[∑n
1ǫ(k)]2}
.
Assumption 6.
For each ﬁnite time interval [0,T], there exists a number A2<∞, independent of n,
such that Var(Sn)≤A2.
Assumption 1 ensures that the uncertainty associated with the unanticipated price
changes is not “washed out” or eliminated even in the limit of continuous trading.
That is, even as h→dt, the “end-of-period” price at time kwill be uncertain relative
to time k−1. This assumption is essential for the continuous-trading model to capture
this fundamental property of stock-price behavior.
Assumption 2 ensures that the uncertainty associated with the unanticipated price
changes over a ﬁnite period of time is not so great that the variance becomes un-
bounded. It rules out the possibility that the very act of allowing more frequent trad-
ing will induce sufﬁcient price instability to cause the limiting variance of X(T)−
X(0)to become unbounded, and it also rules out the Pareto-Levy stable distributions
with inﬁnite variances.
Deﬁne V(k)≡E0{ǫ2(k)},k= 1,2,. . ., n , to be the variance of the dollar return on
the security between time k−1andkbased upon information available as of time
zero, and deﬁne V≡maxkV(k).
Assumption 7.
There exists a number A3,1≥A3>0, independent of n, such that for k= 1,. .. , n ,
V(k)/V≥A3.
6For a formal deﬁnition of the martingale and discussions of its properties, see Feller (1966, pp. 210-15
and 234-8). Important mathematical analyzes of martingales in continuous-time processes are by Dellacherie
and Meyer (1982) and Kunita and Watanabe (1967).
7See Fama (1965a, 1970a, 1991), Samuelson (1965b, 1973), and also Cootner (1964). The theory of
martingales provides a powerful technique for the analysis of equilibrium security prices in continuous-time
models. See Harrison and Kreps (1979), Kreps (1981), Harrison and Pliska (1981, 1983), Dufﬁe and Huang
(1985, 1986), Dufﬁe (1986, 1988), Huang (1985a, b, 1987), Pliska (1986), and Cox and Huang (1989a, b.
1991).
50 On the Mathematics and Economics Assumptions of Continuous-Time Models
Assumption 3 is closely related to Assumption 1 and in effect rules out the possi-
bility that all the uncertainty in the unanticipated price changes over [0,T]is concen-
trated in a few of the many trading periods. In other words, there is signiﬁcant price""",
            """allocations are brieﬂy addressed in Chapter 15 and analyzed more fully in Chapter 16. If a set of existing
securities and markets leads to an equilibrium that is an unconstrained Pareto optimum, then any additional
securities or markets will be redundant.
50The term “transactions costs” can, of course, mean more than just the bid-ask spread or commissions
paid for buying and selling assets. For example, if an investor literally traded his portfolio continuously, he
would have no time to do anything else! Because investment management and ﬁnancial intermediation involve
primarily information processing and security trading, there arc signiﬁcant economies of scale. One would thus
expect substantially lower costs for the individual investor to use intermediaries instead of transacting directly
in the asset markets.
368 Financial Intermediation in the Continuous-Time Model
It would seem therefore that the same dichotomy derived in the frictionless-market
case applies also to our model with transactions costs. In a formal computational
sense it does. We can still solve for the equilibrium asset-price dynamics in the model
of Chapter 15 and then compute the prices of derivative securities, mutual funds, and
corporate liabilities using CCA. There is one signiﬁcant difference, however: the
ﬁrst-part calculation of equilibrium real-sector allocations is valid if and only if there
exists a sufﬁciently rich set of securities and intermediaries in the ﬁnancial sector to
make these allocations feasible for agents who cannot trade without cost. Because
of this conditioning. perhaps a more appropriate term for this separation is “quasi-
dichotomy.”
With the assumption that not all agents can trade continuously without cost, a
signiﬁcant economic role is established for derivative-security markets and ﬁnancial
intermediaries in the model. Somewhat paradoxically, we ﬁnd that, if intermediation
is efﬁcient, then derivative securities and the ﬁnancial products of the intermediaries
will be priced as if they are redundant.51Under these conditions, quasi-dichotomy
obtains, and we can derive equilibrium real-sector allocations and asset prices from
the frictionless-market version of the model.
14.6 Afterword: Policy and Strategy in Financial Intermediation
In this chapter, as throughout the book, the focus has been on theory. Allusions to
practice were concentrated on the micro quantitative applications of the continuous-
time model to product technologies and risk management. Still, I cannot wholly
resist the temptation to call attention to the model’s potential for addressing broader
issues in the practice of intermediation. And so this afterword shall ever so brieﬂy
touch upon implications of the model for intermediation policy and strategy in the
hope that it will lead others, better qualiﬁed, to explore this matter elsewhere.
Derivative securities have long been an integral part of the ﬁnancial markets,52
but most would mark the creation of the Chicago Board Options Exchange in April
1973 as the start of the current wave of ﬁnancial innovations involving derivative
securities. The succeeding years have witnessed an unprecedented proliferation of
organized trading markets in both equity and ﬁxed-income derivative instruments.
In turn, these markets made possible the creation of a wide range of ﬁnancial prod-
51Thus, our model provides a resolution to Hakansson’s (1979, p. 722) “The Catch 22 of Option Pricing.”
Although the equilibrium prices of options and other derivative securities satisfy the redundancy condition of
CCA, they are nevertheless needed to support the equilibrium allocations, and hence their elimination would
reduce social welfare.
52Bernstein (1992) reports that Aristotle’s anecdote about Thales in Book I of Politics is the ﬁrst recorded
mention of a ﬁnancial option. Schaede (1988) makes the case that the Dojima rice market in Osaka was a""",
        ],
    ),
    LLMTestCase(
        input="In simple terms, what does Figure 7 (agent valuations over time) tell us about over‑ vs under‑valuation corrections?",
        actual_output="""Figure 7 shows that the AI agents were better at correcting under-valuations than over-valuations. When the simulated market started low, the agents' valuations gradually increased over time, moving closer to the true fundamental value. However, when the market started high, the agents' valuations remained high and didn't adjust downwards towards the true value within the timeframe of the simulation.
""",
        expected_output="""With an initial price 25 % above fundamentals, prices failed to converge downward within 15 rounds and agents kept over‑valuing the asset.""",
        context=[
            """When the market starts significantly above the fundamental value … the price fails to converge downwards … remaining substantially elevated. Agent valuations mirror this persistence, with many agents maintaining estimates well above the fundamental value."""
        ],
        retrieval_context=[
            """bids/asks), and two Speculator agents (opportunistic traders seeking inefficiencies). Market
31
makers are given enhanced liquidity with 20x the baseline cash and shares to ensure suffi-
cient liquidity provision and facilitate price discovery. The scenario tests whether prices can
correct downward through trading activity when starting from an overvalued state.
3.2.2 Price Discovery (Below Fundamental)
This complementary scenario tests upward price convergence by starting with an initial price
25% below the fundamental value ( $21.00). It employs the identical agent composition and
parameters as the above-fundamental scenario, allowing for direct comparison of market
behavior under opposite initial mispricing conditions. This design enables researchers to
assess potential asymmetries in price discovery processes.
3.2.3 Infinite Horizon Price Discovery
We extend both price discovery scenarios to infinite horizon settings, where shares are not
redeemed at a terminal date. The initial prices are set at double ($56.00) and half ($14.00) the
fundamental value for the above and below fundamental scenarios respectively, creating more
extreme mispricing conditions. These scenarios run for 15 trading rounds and test whether
agents correctly value assets based on expected dividend streams rather than redemption
values. Each infinite horizon scenario involves two Default investors, two Optimistic traders,
two Market makers, and two Speculator agents.
The results from these infinite horizon scenarios reveal interesting asymmetries in price
discovery, as illustrated in Figure 6 and Figure 7. When the market starts significantly above
the fundamental value (left panels), the price fails to converge downwards towards the$28.00
benchmark within the 15 rounds, remaining substantially elevated. Agent valuations mirror
this persistence, with many agents maintaining estimates well above the fundamental value.
However, when the market begins significantly below the fundamental value (right panels),
the price exhibits a clear convergence towards the fundamental benchmark. Agent valuations
in this scenario also tend to adjust upwards, aligning more closely with the calculated fun-
32
damental value over time. This suggests that under these conditions, LLM agents are more
effective at correcting undervaluation than overvaluation within the simulated timeframe.
Figure 6: Price Evolution: Infinite Horizon Scenarios. Left: Initial price $56.00 (Above
Fundamental). Right: Initial price $14.00 (Below Fundamental). The dashed line indicates
the fundamental value ($28.00).
Figure 7: Agent Valuations: Infinite Horizon Scenarios. Left: Initial price $56.00 (Above
Fundamental). Right: Initial price $14.00 (Below Fundamental). Shows individual agent
estimates of fundamental value over time.
3.2.4 Divergent Beliefs
This scenario explores the impact of heterogeneous beliefs about fundamental value by com-
bining agents with systematically different valuation models. The agent composition is
designed to create heterogeneity: two Optimistic traders (believing the fundamental value is
significantly higher), two Pessimistic traders (believing it is significantly lower), two neutral
Market makers, two Momentum traders (following price trends rather than fundamentals),
and two Default investors (baseline agents). We test both above-fundamental (initial price
$56.00, 2x fundamental) and below-fundamental (initial price$14.00, 0.5x fundamental) vari-
33
ants, allowing researchers to study how different belief structures influence price formation
and trading patterns under different initial mispricings. In these scenarios, the fundamental
price is hidden from agents, forcing them to rely on their own valuation models.
3.2.5 Market Stress
This scenario tests market resilience under challenging conditions by creating a more volatile
environment. The scenario includes two consistently bullish Optimistic traders, two consis-""",
            """value, the system:
1. Sets market price P = ρV where ρ is the target ratio
2. Generates a consistent order book structure around this price
3. Executes multiple decision trials with the same agent type
4. Records decision outcomes (buy/sell/hold), order types, quantities, and reasoning
This process maps how LLM agents respond to different price environments, as illustrated
in Figures 2, 3, 4, and 5. The analysis reveals clear patterns in decision boundaries, with
distinct transitions between buying, selling, and holding regions that vary by agent type. For
example, value investors show strong buying tendencies when prices are below fundamental
value (ρ <1) and selling preferences when prices exceed fundamentals ( ρ >1). In contrast,
momentum traders show less sensitivity to the fundamental ratio and more responsiveness
to recent price trends.
The systematic variation approach also reveals patterns in order sizing and limit price
selection, with agents typically placing larger orders when prices deviate significantly from
their valuation models (Figure 4). This methodology provides unprecedented transparency
into LLM decision processes and enables quantitative comparison of different agent types
and LLM architectures.
22
Figure 2: Price Analysis under Systematic Variation. Shows how agent valuation estimates
and price targets respond to varying Price/Fundamental ratios.
The decision analysis can be customized for different experimental designs. For example,
researchers can use the framework to study the impact of various market conditions on agent
behavior by varying other market parameters or the effect of different agent types on market
dynamics by changing the agent population.
2.3 Data Collection and Analysis
Evaluating LLM trading agents requires robust methodologies for capturing, processing,
and analyzing their behavior in market environments. The framework implements a com-
prehensive analytics module that tracks all market activity, agent decisions, and performance
metrics throughout experimental runs. This multi-layered approach not only records what
happens in each simulation but also provides insights into why agents make specific deci-
sions, enabling researchers to validate agent behavior against their defined strategies and
assess overall market dynamics. The following sections detail the key components of this
analytics infrastructure.
23
Figure 3: Trading Decision Distribution under Systematic Variation. Illustrates the proba-
bility of Buy, Sell, or Hold decisions across different agent types as the Price/Fundamental
ratio changes.
24
Figure 4: Order Size Distribution under Systematic Variation. Shows the average quan-
tity traded (as a percentage of initial shares) for Buy and Sell orders across different
Price/Fundamental ratios.
2.3.1 Data Collection Architecture
The framework implements a comprehensive data collection system that captures multiple
dimensions of market behavior and agent decision-making. This structured approach ensures
reproducibility and enables detailed analysis of market dynamics.
2.3.2 Core Data Streams
The system captures five primary data streams that work together to provide a complete
picture of market activity. Market Data forms the foundation, tracking essential metrics
including price evolution, fundamental values, trading volumes, order book depth, market
liquidity, best bid/ask prices, spreads, and price-fundamental ratios. This is complemented
by detailed Trade Data, which records individual transaction details such as prices, quan-
tities, buyer and seller identifiers, timestamps, round information, and specific execution
details.
Agent Data provides insights into participant behavior by monitoring cash and share
25
Figure 5: Order Type Analysis under Systematic Variation. Displays the proportion of
Market vs. Limit orders used by different agent types across varying Price/Fundamental
ratios.
26""",
            """the decision-making engine.
The data collection system captures comprehensive market activity across multiple di-
mensions. At the market level, it tracks the evolution of prices, fundamental values, and
realized dividends, providing insights into overall market dynamics. Individual agent data
includes detailed wealth trajectories and portfolio compositions, enabling analysis of strategy
effectiveness and wealth distribution patterns. The system maintains complete transaction
records with prices, quantities, and counterparty information, facilitating the study of trad-
ing patterns and market microstructure. Additionally, it captures agent decision rationales
and strategy adherence metrics, allowing researchers to evaluate the consistency and effec-
tiveness of different trading approaches.
All experimental parameters, market outcomes, and agent interactions are systemati-
cally logged and stored in structured formats (CSV and JSON) for subsequent analysis. The
framework generates standardized visualizations of price evolution, wealth distribution, and
dividend payments to facilitate comparative analysis across different experimental configu-
rations.
3.1 Fundamental Value Calibration
The framework implements a consistent approach to fundamental value calculation that pro-
vides a reliable benchmark for price discovery. For infinite horizon markets, the fundamental
value follows the standard dividend discount model:
Vt = E[D]
r = Expected Dividend
Interest Rate (1)
For the default parameters where the expected dividend is $1.40 and the interest rate is
5%, this yields a fundamental value of $28.00.
In finite horizon markets with T periods remaining, the fundamental value incorporates
30
both future dividends and terminal redemption value K:
FVt =
TX
τ=t
E[D]
(1 + r)τ−t+1 + K
(1 + r)T−t+1 (2)
To ensure consistency between finite and infinite horizon markets, the redemption value
K is set equal to E[D]
r , which makes the fundamental value constant atE[D]
r across all periods,
regardless of the time horizon. This calibration approach ensures a clean experimental design
by providing a stable benchmark for price discovery.
3.2 Experimental Scenarios
To evaluate market dynamics with LLM-based agents, we implemented several experimental
scenarios that systematically explore different initial conditions and agent compositions.
Each scenario maintains the fundamental value of $28.00 while varying starting prices, time
horizons, and agent populations. These scenarios address our core research questions (Section
1) by testing LLM capabilities under varying market conditions, focusing on price discovery
dynamics, the impact of heterogeneous beliefs, and market stability under stress; GPT-4o
was used consistently as the decision-making engine for all LLM agents across these scenarios.
We present the setup for several key scenarios below, followed by a discussion of the observed
results for the 2 experiments involving an infinite horizon market with a starting price either
above or below the fundamental value.
3.2.1 Price Discovery (Above Fundamental)
This scenario tests downward price convergence by starting with an initial price 25% above
the fundamental value ( $35.00). It runs for 20 trading rounds and features a diverse
agent population, including two Default investors (baseline agents), two Optimistic traders
(who believe prices should be higher), two Market makers (providing liquidity by posting
bids/asks), and two Speculator agents (opportunistic traders seeking inefficiencies). Market
31
makers are given enhanced liquidity with 20x the baseline cash and shares to ensure suffi-
cient liquidity provision and facilitate price discovery. The scenario tests whether prices can
correct downward through trading activity when starting from an overvalued state.
3.2.2 Price Discovery (Below Fundamental)
This complementary scenario tests upward price convergence by starting with an initial price""",
            """market efficiency and price discovery processes throughout the simulation.
Agent performance metrics include absolute position tracking (shares, cash, and total
wealth), wealth composition analysis, position change metrics, and return calculations. The
system computes both absolute and percentage returns on various portfolio components
and compares performance across agent types to identify relative advantages of different
strategies. Trading flow analysis visualizes the volume of shares moving between different
agent types and cumulative net trading flows, revealing which agents act as net buyers or
sellers in different market conditions.
Decision pattern analysis employs heatmaps to visualize the consistency of agent decision-
making over time, allowing researchers to identify shifts in strategic behavior. This is com-
plemented by decision quantities visualization that plots order sizes to highlight variations
in trade aggressiveness across agent types. When agent reasoning data is available, the
system generates wordclouds to extract key terms from agent explanations, providing qual-
itative insights into decision drivers for different agent strategies. Additional visualizations
track price target accuracy and compare agent-specific valuations to realized market prices,
28
offering insights into the forecasting abilities of different agents.
A key advantage of simulation-based analysis is complete observability of all market
processes and agent states. Unlike real-world markets where data availability is often limited,
the framework captures every interaction, decision, and state change with perfect fidelity.
This comprehensive data collection allows researchers to compute additional metrics beyond
standard market measures, enabling novel analyses such as counterfactual testing (e.g., how
would markets evolve with different agent compositions), causal inference of specific agent
behaviors on market outcomes, and the development of custom efficiency or stability metrics
tailored to particular research questions. The system’s modular design facilitates rapid
implementation of new metrics and visualizations as research questions evolve.
3 Experimental Design and Results
Our experimental framework implements a dividend-paying asset market with heterogeneous
agents. The baseline simulation runs for 15 to 20 rounds with 8 participating agents, although
these parameters are fully configurable. Each agent begins with an initial endowment of
1,000,000 monetary units and 10,000 shares of the asset. The fundamental value of the asset
is set at $28.00, with a final redemption value matching this fundamental price in finite
horizon scenarios. Transaction costs are set to zero to isolate the effects of agent behavior
and market structure.
The dividend structure follows a stochastic process with a base payment of $1.40 and a
variation of ±$1.00, paid with 50% probability each round. This design creates uncertainty
in the asset’s income stream while maintaining a known expected value. Cash holdings earn
a risk-free interest rate of 5% per round, providing an opportunity cost for asset investment.
Agent composition is controlled through a flexible distribution system that allows for
various experimental configurations. In our baseline setup, we employ a mixed population
of value investors, momentum traders, and market makers. Each agent type implements
29
distinct trading strategies through Large Language Model (LLM) prompts, with GPT-4o as
the decision-making engine.
The data collection system captures comprehensive market activity across multiple di-
mensions. At the market level, it tracks the evolution of prices, fundamental values, and
realized dividends, providing insights into overall market dynamics. Individual agent data
includes detailed wealth trajectories and portfolio compositions, enabling analysis of strategy
effectiveness and wealth distribution patterns. The system maintains complete transaction""",
            """by detailed Trade Data, which records individual transaction details such as prices, quan-
tities, buyer and seller identifiers, timestamps, round information, and specific execution
details.
Agent Data provides insights into participant behavior by monitoring cash and share
25
Figure 5: Order Type Analysis under Systematic Variation. Displays the proportion of
Market vs. Limit orders used by different agent types across varying Price/Fundamental
ratios.
26
positions, portfolio values, wealth evolution, and agent type and strategy identifiers. Or-
der Data captures the complete lifecycle of trading decisions, including order specifications
(type, size, price), agent reasoning and justification, decision context and timing, and order
lifecycle events. Finally, Market State data maintains a comprehensive view of overall mar-
ket conditions through order book snapshots, market depth information, aggregate statistics,
and various market microstructure metrics.
2.3.3 Data Validation and Storage
The system implements a comprehensive set of data quality measures to ensure reliability and
consistency. The validation framework performs continuous checks for data completeness,
verifies consistency across related data streams, enforces format and type validation, and
maintains proper temporal sequencing of all recorded events. These validation mechanisms
work together to maintain data integrity throughout the experimental process.
The storage architecture employs multiple formats optimized for different data types and
use cases. Structured CSV files store tabular data for efficient analysis, while JSON formats
accommodate complex nested structures that preserve the rich relationships between market
elements. The system maintains detailed timestamped logs for debugging purposes and
generates summary statistics to facilitate quick analysis of experimental outcomes.
This comprehensive data collection architecture enables researchers to conduct detailed
analysis of market dynamics, validate agent behavior patterns, ensure experiment repro-
ducibility, and perform meaningful cross-experiment comparisons. The integrated approach
to data management provides the foundation for rigorous empirical investigation of market
behavior and agent interactions.
The framework implements specialized visualization techniques to analyze agent behavior
and market dynamics. Decision heatmaps plot agent actions across trading rounds, reveal-
ing strategic patterns and consistency. Trading flow visualizations track cumulative position
changes, identifying net buyers and sellers throughout market evolution. Reasoning word-
27
clouds extract key terms from agent explanations, providing insight into decision drivers
across different agent types.
The system also generates specialized market quality visualizations including bid-ask
spread evolution, price target accuracy, and agent valuation tracking. These visualizations
work in concert with the numerical metrics to provide both quantitative and qualitative
insights into agent behavior and market dynamics.
2.3.4 Validation Metrics and Performance Monitoring
The framework implements a comprehensive set of performance metrics and visualization
tools that monitor agent behavior and market dynamics. Market evolution visualizations
track price movements relative to fundamental values, including time series of transaction
prices, midpoint prices, and bid-ask spreads. These visualizations enable researchers to assess
market efficiency and price discovery processes throughout the simulation.
Agent performance metrics include absolute position tracking (shares, cash, and total
wealth), wealth composition analysis, position change metrics, and return calculations. The
system computes both absolute and percentage returns on various portfolio components
and compares performance across agent types to identify relative advantages of different""",
            """the second agents’ design, and the third the analysis module.
8
2.1 Market Design
Our methodological framework integrates three components that create a controlled envi-
ronment for LLM-based trading agents. The framework implements a flexible continuous
double-auction market mechanism that couples standard market microstructure principles
with market clearing and matching algorithms to accommodate asynchronous LLM decisions.
The market clearing process employs a dual-stage matching algorithm. In the first stage,
limit orders are posted. In the second stage, market orders are netted using a market-
to-market matching engine that processes buy and sell orders, reconciling orders based on
available agent cash and share commitments. In the third stage, any remaining market
orders are matched against the existing order book, with unfilled quantities converted to
aggressive limit orders. This three-tiered approach optimizes immediate execution and price
discovery while maintaining market liquidity.
The system’s OrderMatchingService orchestrates this process by coordinating trade ex-
ecutions through the TradeExecutionService and managing order state transitions via the
OrderStateManager. Each trade is logged in detail, with the overall market state—including
order books, market depth, and price evolution—recalculated at the end of each trading
round.
This modular design in the matching and clearing engine provides several advantages.
First, it enables rigorous trade validation where each market order is validated against agent
cash commitments and position constraints before matching, with the system dynamically
adjusting order quantities based on available cash when an agent’s commitment is insuf-
ficient, thus minimizing execution errors. Second, it offers flexible liquidity handling by
supporting market-to-market and market-to-book matching, ensuring orders have multiple
execution pathways, with unexecuted market orders converted to aggressive limit orders to
capture remaining liquidity. Third, it maintains detailed trade audit capabilities by recording
comprehensive traceability data including timestamps, trade volumes, executed prices, and
agent identifiers, thereby enabling post-trade analysis and performance benchmarking that
9
serves as the foundation for subsequent market efficiency and agent performance validations.
2.1.1 Market Mechanism Design
Our framework implements a continuous double-auction market mechanism that processes
orders in discrete trading rounds. We use discrete trading rounds because LLMs have latency
constraints, making it infeasible to process orders in real time. Within each round, the order
of agent submissions is randomized to avoid giving systematic priority to specific agents,
thus simulating concurrent order arrival while maintaining fairness. Once randomized, or-
ders are then processed according to standard price-time priority rules. The system supports
finite and infinite horizon markets, with differences in terminal conditions and wealth cal-
culation. In finite-horizon markets, agents are informed of the total number of rounds, and
their terminal wealth is calculated by redeeming all shares at the fundamental value of the
final round. In infinite-horizon markets, no terminal information is provided to agents, and
final wealth is determined using the last market price for share valuation. This design choice
enables researchers to study how time horizons influence trading strategies and price for-
mation, particularly how agents balance short-term trading opportunities against long-term
value considerations.
In a double auction, buyers and sellers actively submit orders, with trades occurring when
compatible buy and sell orders match the price. The matching engine processes these orders
through three sequential phases:
First, incoming limit orders that do not immediately cross the market are added to
the order book, maintaining strict price-time priority. Second, market orders are processed""",
            """33
ants, allowing researchers to study how different belief structures influence price formation
and trading patterns under different initial mispricings. In these scenarios, the fundamental
price is hidden from agents, forcing them to rely on their own valuation models.
3.2.5 Market Stress
This scenario tests market resilience under challenging conditions by creating a more volatile
environment. The scenario includes two consistently bullish Optimistic traders, two consis-
tently bearish Pessimistic traders, two Market makers (liquidity providers), and two Value
investors (rational benchmark traders). The scenario runs for 100 rounds to study long-term
market behavior and includes unequal initial endowments, with optimistic traders having
more cash (1.5x baseline) but fewer shares (0.5x baseline) and pessimistic traders having less
cash (0.5x baseline) but more shares (1.5x baseline). This resource imbalance tests whether
particular agent types can dominate market outcomes through resource advantages.
The scenarios presented here demonstrate the framework’s capabilities for exploring di-
verse market conditions. Its modular structure facilitates the straightforward definition and
implementation of alternative experimental designs, enabling researchers to tailor simulations
to specific research questions.
In all scenarios, we maintain consistent baseline parameters with a fundamental value
of $28.00, calculated from the expected dividend of $1.40 and interest rate of 5%. Agent
endowments start at 1,000,000 monetary units and 10,000 shares unless specifically modified.
Transaction costs are set to zero to isolate the effects of agent behavior and market structure
on price formation.
4 Conclusion
This paper demonstrates that Large Language Models can effectively function as diverse
trading agents—from value investors to market makers—maintaining strategic consistency
34
while adapting to market conditions. Our experimental framework reveals that their in-
teractions generate realistic market dynamics, including phenomena like price bubbles and
corrections, highlighting both the capabilities and potential risks of deploying LLM agents
in financial markets.
These findings carry significant implications for market structure and regulation. While
LLM agents can enhance price discovery and liquidity, their adherence to programmed strate-
gies, even potentially flawed ones derived from prompts, could amplify market volatility or
introduce novel systemic risks, as observed in our simulated bubble scenarios. A key concern
is the potential for widespread correlated behavior: similar underlying LLM architectures
responding uniformly to comparable prompts or market signals could inadvertently create
destabilizing trading patterns without explicit coordination. This underscores the critical
need for rigorous testing and validation of LLM-based trading systems prior to live deploy-
ment.
A central contribution of this work is the open-source simulation framework itself, de-
signed to catalyze research into LLM trading agents. We invite the research community to
utilize and extend this platform to investigate pressing questions in this rapidly evolving
area. The framework enables systematic exploration of complex scenarios—such as hybrid
human-LLM markets, stress tests, varying market structures, regulatory impacts, and the
nuances of LLM prompting—often difficult or costly to study otherwise. Specific avenues
ripe for investigation using this tool include the emergence of novel trading strategies, the
precise effects of agent heterogeneity on market stability, and the development of robust
validation protocols for AI traders. As artificial intelligence becomes more integrated into
finance, collaborative research leveraging adaptable simulation environments like this one
will be crucial for understanding and responsibly shaping the future of trading.
35
References""",
            """(2023)). This work, however, focuses on financial markets and how LLM agents can operate
as full-fledged trading participants.
Recent research examines specific applications of LLMs for trading. FinMem and Trad-
ingGPT introduce frameworks with layered memory systems and customizable agent traits
5
to improve financial decision-making (Yu, Li, et al. 2024; Li, Zhang, and Sun 2023). Hierar-
chical multi-agent architectures have been explored in FinCon, which uses a manager-analyst
setup for collaborative portfolio decisions (Yu, Yao, et al. 2024). QuantAgent implements
a self-improving signal-mining approach (Wang et al. 2024), while other work underscores
the importance of long-term memory in LLM agents via vector databases (Hatalis et al.
2024). This line of research builds on successful reinforcement learning applications such as
AlphaPortfolio (Cong et al. 2021) and AlphaManager (Campello, Cong, and Zhou 2023),
which leverage deep RL and robust control for portfolio management.
Analyzing LLM agent behavior by changing only some parameters draws on methods
from the interpretable machine learning literature. In particular, the systematic variation
of market parameters to reveal decision patterns mirrors partial dependence plots and in-
dividual conditional expectation curves used to interpret complex machine learning models
(Molnar 2022). These techniques help reveal how LLM agents respond to changes in specific
variables while holding others constant, providing insight into their internal decision-making
processes that would otherwise remain opaque.
Beyond finance, studies of LLM capabilities in interactive or multi-agent settings offer
valuable insights. Benchmarks like AgentBench evaluate LLMs’ performance in interac-
tive tasks (Liu et al. 2023), while InvestorBench focuses on financial decision-making tasks
specifically (H. Li et al. 2024). NegotiationArena demonstrates LLMs’ capacity for strategic
interaction in bargaining contexts (Bianchi et al. 2024). Similarly, Guo et al. (2024) provide
an economics ”arena” where LLMs compete in strategic games, revealing that advanced
models like GPT-4 can exhibit rational, adaptive behavior—albeit not always reaching Nash
Equilibrium. Existing frameworks typically assess individual agents or hierarchical collab-
orations, whereas this work studies emergent market behaviors that arise from multiple
independent LLM traders interacting in a marketplace.
The approach also connects to the tradition of experimental asset markets. For instance,
Weitzel et al. (2020) show that even finance professionals are susceptible to speculative
6
bubbles, especially amid high capital inflows. Kop´ anyi-Peuker and Weber (2021) find that
trading experience alone does not eliminate bubbles, challenging assumptions about rational
market learning. Kirchler, Huber, and St¨ ockl (2012) identify confusion about fundamental
values as a key driver of bubble formation. This framework offers a new way to study these
phenomena with LLM traders, which can be rigorously parameterized for sophistication,
strategy, and information processing. Hence, this paper provides a method to investigate
how automated or ”artificial” agents might affect market stability or volatility.
Other recent work highlights the versatility of LLM agents in complex, interactive sce-
narios beyond finance. One stream focuses on simulating social behaviors—such as opinion
dynamics (Chuang et al. 2023), trust (Xie et al. 2024), and resource-sharing (Piatti et al.
2024). Another examines LLMs’ strategic capabilities through task-based simulations and
collaborative decision-making (Li, Zhang, and Sun 2023; Piatti et al. 2024).
Within the computer science literature, early works apply LLMs to financial markets but
abstract away many fundamental stock market characteristics. Often, they employ single-
price clearing mechanisms without a persistent order book, ignore partial fills and bid-ask""",
        ],
    ),
    LLMTestCase(
        input="Why is short selling prohibited for these agents, and how might allowing it change the results?",
        actual_output="""Short selling is prohibited to simplify the simulation and avoid potentially destabilizing effects that short selling can introduce, especially given the experimental nature of using LLMs (Large Language Models) as trading agents. The authors wanted to focus on the core dynamics of price discovery without the added complexity of short selling.

Allowing short selling could significantly change the results in several ways:

Increased Downward Pressure on Prices: If agents could short sell, they could put more downward pressure on prices when they believe the asset is overvalued. This might lead to faster and more efficient corrections of overvaluations, potentially mitigating the persistent overvaluation observed in the simulations.
Increased Market Volatility: Short selling can amplify both upward and downward price movements, making the market more volatile. This is because short sellers can create additional selling pressure, driving prices down further and faster than would be possible with only long positions (owning the asset). Conversely, covering short positions (buying back borrowed shares to close a short position) can lead to rapid price increases.
More Complex Agent Strategies: Allowing short selling would open up a wider range of possible trading strategies for the agents. They could implement strategies like short and distort (betting against overvalued assets), pairs trading (simultaneously buying an undervalued asset and shorting an overvalued one), or other more sophisticated approaches. This increased complexity could make it more difficult to interpret the agents' behavior and understand the underlying market dynamics.
Potential for Market Manipulation: While not explicitly mentioned, the possibility of market manipulation through short selling could become a factor, especially given the experimental nature of the agents. This could take the form of aggressively shorting an asset to drive down its price, potentially creating artificial price crashes or exacerbating existing downturns.
""",
        expected_output="""It shows asymmetry: over‑valuation persists, but under‑valuation is corrected—the right panel converges to $28 while the left stays high.""",
        context=[
            """When the market starts significantly above the fundamental value … the price fails to converge downwards … remaining substantially elevated. Agent valuations mirror this persistence, with many agents maintaining estimates well above the fundamental value."""
        ],
        retrieval_context=[
            """2407.18957. arXiv: 2407.18957 [q-fin]. http://arxiv.org/abs/2407.18957.
41
A Technical Implementation Details
A.1 Agent Type Specifications
This section details the base system prompts for each agent type in our simulation. These
prompts define the core behavioral characteristics and trading strategies for each agent. Each
prompt consists of:
• A role definition that establishes the agent’s trading philosophy
• A structured trading strategy that guides decision-making
• Specific instructions for when to use market orders vs limit orders
At runtime, these base prompts are combined with:
• Current market state (price, volume, order book depth)
• Position information (current holdings and available cash)
• Trading options and required response format
The standard runtime template includes:
Position Information Template
Your Position:
- Available Shares: {shares} shares (Short selling is not allowed)
- Main Cash Account: ${cash:.2f}
- Dividend Cash Account (not available for trading): ${dividend_cash:.2f}
- Total Available Cash: ${total_available_cash:.2f} (Borrowing is not allowed)
- Shares in Orders: {committed_shares} shares
- Cash in Orders: ${committed_cash:.2f}
42
Trading Options Template
Your analysis should include:
- valuation_reasoning: Your numerical analysis of the asset’s fundamental value
- valuation: Your estimate of the asset’s current fundamental value
- price_target_reasoning: Your numerical analysis of the asset’s price target
- price_target: Your predicted price for the next round
- reasoning: Your explanation for the trading decision
Trading Options:
1. New Orders (replace_decision=’Add’):
- Single or multiple orders allowed
- For each order:
- Market order: Set order_type=’market’
- Limit order: Set order_type=’limit’ and specify price_limit
- IMPORTANT: Sell orders require sufficient available shares
- Short selling is NOT allowed
2. Cancel Orders (replace_decision=’Cancel’):
- Return an empty orders list: orders=[]
Your decision must include:
- orders: list of orders (empty list for Hold/Cancel)
- For Buy/Sell orders, each must contain:
- decision: "Buy" or "Sell"
- quantity: number of shares
- order_type: "market" or "limit"
- price_limit: required for limit orders
- reasoning: brief explanation
- replace_decision: "Add", "Cancel", or "Replace"
43
Base System Prompts The following are the base system prompts for each LLM-based
agent type:
A.1.1 Value-Based Agents
Value Investor
You are a value investor who focuses on fundamental analysis.
You believe in mean reversion and try to buy undervalued assets and sell overvalued ones.
A.1.2 Trend-Following Agents
Momentum Trader
You are a momentum trader who focuses on price trends and volume.
You believe that ’the trend is your friend’ and try to identify and follow market momentum.
A.1.3 Liquidity Providers Agents
Market Maker
You are a professional market maker who provides liquidity to the market.
Your profit comes from capturing the spread between bid and ask prices, not from directional price movement.
IMPORTANT: There is NO SHORT SELLING allowed. You can only sell shares you already own.
Trading Guidelines:
- Place LIMIT buy orders slightly below the current market price (1-3% lower)
- Place LIMIT sell orders slightly above the current market price (1-3% higher)
- Your spread should be proportional to volatility but typically 2-6% of price
- NEVER place sell orders more than 10% above your buy orders
- Adjust your spread width based on recent price volatility
44
Inventory Management (No Short Selling):
- Monitor your current inventory in the market data
- Only place sell orders for quantities you actually own
- If you have no inventory, focus on buy orders first
- As you acquire inventory, gradually place sell orders
- If inventory grows too large, reduce or pause buy orders
- Adjust your buy/sell ratio based on current inventory level
Example: If price = $100, you might place buy orders at $97-99 and sell orders at $101-103,""",
            """33
ants, allowing researchers to study how different belief structures influence price formation
and trading patterns under different initial mispricings. In these scenarios, the fundamental
price is hidden from agents, forcing them to rely on their own valuation models.
3.2.5 Market Stress
This scenario tests market resilience under challenging conditions by creating a more volatile
environment. The scenario includes two consistently bullish Optimistic traders, two consis-
tently bearish Pessimistic traders, two Market makers (liquidity providers), and two Value
investors (rational benchmark traders). The scenario runs for 100 rounds to study long-term
market behavior and includes unequal initial endowments, with optimistic traders having
more cash (1.5x baseline) but fewer shares (0.5x baseline) and pessimistic traders having less
cash (0.5x baseline) but more shares (1.5x baseline). This resource imbalance tests whether
particular agent types can dominate market outcomes through resource advantages.
The scenarios presented here demonstrate the framework’s capabilities for exploring di-
verse market conditions. Its modular structure facilitates the straightforward definition and
implementation of alternative experimental designs, enabling researchers to tailor simulations
to specific research questions.
In all scenarios, we maintain consistent baseline parameters with a fundamental value
of $28.00, calculated from the expected dividend of $1.40 and interest rate of 5%. Agent
endowments start at 1,000,000 monetary units and 10,000 shares unless specifically modified.
Transaction costs are set to zero to isolate the effects of agent behavior and market structure
on price formation.
4 Conclusion
This paper demonstrates that Large Language Models can effectively function as diverse
trading agents—from value investors to market makers—maintaining strategic consistency
34
while adapting to market conditions. Our experimental framework reveals that their in-
teractions generate realistic market dynamics, including phenomena like price bubbles and
corrections, highlighting both the capabilities and potential risks of deploying LLM agents
in financial markets.
These findings carry significant implications for market structure and regulation. While
LLM agents can enhance price discovery and liquidity, their adherence to programmed strate-
gies, even potentially flawed ones derived from prompts, could amplify market volatility or
introduce novel systemic risks, as observed in our simulated bubble scenarios. A key concern
is the potential for widespread correlated behavior: similar underlying LLM architectures
responding uniformly to comparable prompts or market signals could inadvertently create
destabilizing trading patterns without explicit coordination. This underscores the critical
need for rigorous testing and validation of LLM-based trading systems prior to live deploy-
ment.
A central contribution of this work is the open-source simulation framework itself, de-
signed to catalyze research into LLM trading agents. We invite the research community to
utilize and extend this platform to investigate pressing questions in this rapidly evolving
area. The framework enables systematic exploration of complex scenarios—such as hybrid
human-LLM markets, stress tests, varying market structures, regulatory impacts, and the
nuances of LLM prompting—often difficult or costly to study otherwise. Specific avenues
ripe for investigation using this tool include the emergence of novel trading strategies, the
precise effects of agent heterogeneity on market stability, and the development of robust
validation protocols for AI traders. As artificial intelligence becomes more integrated into
finance, collaborative research leveraging adaptable simulation environments like this one
will be crucial for understanding and responsibly shaping the future of trading.
35
References""",
            """44
Inventory Management (No Short Selling):
- Monitor your current inventory in the market data
- Only place sell orders for quantities you actually own
- If you have no inventory, focus on buy orders first
- As you acquire inventory, gradually place sell orders
- If inventory grows too large, reduce or pause buy orders
- Adjust your buy/sell ratio based on current inventory level
Example: If price = $100, you might place buy orders at $97-99 and sell orders at $101-103,
but limit your sell quantity to what you currently own.
Remember that extreme spreads (e.g., buying at $3 and selling at $30) will not execute and will lead to losses.
A.1.4 Contrarian Agents
Contrarian Trader
You are a contrarian trader who looks for excessive market moves to trade against.
You believe markets often overreact and try to profit from reversals.
A.1.5 Sentiment-Based Agents
Optimistic
You are an optimistic trader who firmly believes assets are significantly undervalued.
Your Core Beliefs:
- The probability of maximum dividends is much higher than stated (80-90% chance)
Pessimistic
You are a pessimistic trader who firmly believes assets are significantly overvalued.
45
Your Core Beliefs:
- The probability of minimum dividends is much higher than stated (80-90% chance)
A.1.6 Miscellaneous Agents
Speculator
You are a speculator who tries to profit from market inefficiencies.
Retail Trader
You are a retail trader.
LLM Hold Trader
You are a holding agent that never trades.
A.1.7 Deterministic Agents
The framework also includes several deterministic rule-based agents that serve as benchmarks
and controls. These agents follow fixed algorithmic rules rather than LLM-based decision-
making. They include directional traders (always buy, always sell), technical traders (mean
reversion, momentum), and algorithmic market makers with pre-defined spread-posting
strategies.
46""",
            """standardized, human-readable, machine-readable agent decisions. This technique allows
LLMs to generate outputs in a specific format that can be directly validated and processed
by the trading system, bridging the gap between natural language reasoning and executable
trading actions.
The system uses Pydantic for validation and parsing of agent outputs, with a schema-
based approach that defines the required structure:
class TradeDecisionSchema(BaseModel):
Schema for trade decisions
valuation_reasoning: str = Field(...,
description="Brief explanation of valuation analysis")
valuation: float = Field(...,
description="Agent’s estimated fundamental value")
price_target: float = Field(...,
description="Agent’s predicted price in near future")
orders: List[OrderSchema] = Field(...,
description="List of orders to execute")
16
replace_decision: str = Field(...,
description="Add, Cancel, or Replace")
reasoning: str = Field(...,
description="Explanation for the trading decisions")
Each order within the decision follows a nested schema:
class OrderSchema(BaseModel):
Schema for individual orders
decision: Literal["Buy", "Sell"] = Field(...,
description="Buy, Sell")
quantity: int = Field(...,
description="Number of shares")
order_type: str = Field(...,
description="market or limit")
price_limit: Optional[float] = Field(None,
description="Required for limit orders")
This structured approach enables several critical features: (1) automatic validation of all
decision components, (2) consistent parsing of agent outputs, (3) clear documentation of the
expected response format, and (4) standardized error handling for malformed responses. The
function calling methodology ensures that LLMs can focus on trading strategy. At the same
time, the system handles the technical validation of their decisions, significantly improving
reliability compared to free-form text parsing.
2.2.7 Complete Example
The following example illustrates the complete prompt for a speculator agent, with annota-
tions explaining the purpose of each information component.
You are a speculator who tries to profit from market inefficiencies.
17
The system prompt establishes the agent’s core identity and strategic objective concisely,
creating a consistent behavioral foundation. Then, the user prompt provides the immediate
market context necessary for tactical decision-making.
2.2.8 Market State Information
Market State:
Last Price: $29.00
Round Number: 4/Infinite
Best Public Estimate of Risk-Neutral Fundamental Value: Unavailable
Last Trading Volume: 500.00
Price/Fundamental Ratio: Unavailable
This subsection provides essential market pricing data to establish current conditions. The
speculator intentionally receives no fundamental value estimate to simulate information
asymmetry and encourage independent analysis.
2.2.9 Market Depth
Market Depth:
Best Bid: $28.00
Best Ask: $29.00
Sell Orders:
2000 shares @ $57.00
3800 shares @ $50.40
2000 shares @ $30.00
1000 shares @ $29.50
4400 shares @ $29.00
Buy Orders:
1900 shares @ $28.00
18
1500 shares @ $27.50
2500 shares @ $27.00
Order book information lets the agent assess market liquidity, identify potential trading
opportunities, and determine optimal order placement strategies. The visible imbalance
between the bid and ask sides provides critical information about supply and demand dy-
namics.
2.2.10 Agent Position
Your Outstanding Orders:
Buy Orders:
400 shares @ $28.00
Your Position:
Available Shares: 10000 shares (Short selling is not allowed)
Main Cash Account: $988500.00
Dividend Cash Account (not available for trading): $296920.65
Total Available Cash: $988500.00 (Borrowing is not allowed)
Shares in Orders: 0 shares
Cash in Orders: $11500.00
Position information establishes resource constraints and current market exposure, enabling
the agent to make contextually appropriate decisions while maintaining awareness of out-
standing commitments.
2.2.11 Historical Context
Price History (last 5 rounds):""",
            """(2023)). This work, however, focuses on financial markets and how LLM agents can operate
as full-fledged trading participants.
Recent research examines specific applications of LLMs for trading. FinMem and Trad-
ingGPT introduce frameworks with layered memory systems and customizable agent traits
5
to improve financial decision-making (Yu, Li, et al. 2024; Li, Zhang, and Sun 2023). Hierar-
chical multi-agent architectures have been explored in FinCon, which uses a manager-analyst
setup for collaborative portfolio decisions (Yu, Yao, et al. 2024). QuantAgent implements
a self-improving signal-mining approach (Wang et al. 2024), while other work underscores
the importance of long-term memory in LLM agents via vector databases (Hatalis et al.
2024). This line of research builds on successful reinforcement learning applications such as
AlphaPortfolio (Cong et al. 2021) and AlphaManager (Campello, Cong, and Zhou 2023),
which leverage deep RL and robust control for portfolio management.
Analyzing LLM agent behavior by changing only some parameters draws on methods
from the interpretable machine learning literature. In particular, the systematic variation
of market parameters to reveal decision patterns mirrors partial dependence plots and in-
dividual conditional expectation curves used to interpret complex machine learning models
(Molnar 2022). These techniques help reveal how LLM agents respond to changes in specific
variables while holding others constant, providing insight into their internal decision-making
processes that would otherwise remain opaque.
Beyond finance, studies of LLM capabilities in interactive or multi-agent settings offer
valuable insights. Benchmarks like AgentBench evaluate LLMs’ performance in interac-
tive tasks (Liu et al. 2023), while InvestorBench focuses on financial decision-making tasks
specifically (H. Li et al. 2024). NegotiationArena demonstrates LLMs’ capacity for strategic
interaction in bargaining contexts (Bianchi et al. 2024). Similarly, Guo et al. (2024) provide
an economics ”arena” where LLMs compete in strategic games, revealing that advanced
models like GPT-4 can exhibit rational, adaptive behavior—albeit not always reaching Nash
Equilibrium. Existing frameworks typically assess individual agents or hierarchical collab-
orations, whereas this work studies emergent market behaviors that arise from multiple
independent LLM traders interacting in a marketplace.
The approach also connects to the tradition of experimental asset markets. For instance,
Weitzel et al. (2020) show that even finance professionals are susceptible to speculative
6
bubbles, especially amid high capital inflows. Kop´ anyi-Peuker and Weber (2021) find that
trading experience alone does not eliminate bubbles, challenging assumptions about rational
market learning. Kirchler, Huber, and St¨ ockl (2012) identify confusion about fundamental
values as a key driver of bubble formation. This framework offers a new way to study these
phenomena with LLM traders, which can be rigorously parameterized for sophistication,
strategy, and information processing. Hence, this paper provides a method to investigate
how automated or ”artificial” agents might affect market stability or volatility.
Other recent work highlights the versatility of LLM agents in complex, interactive sce-
narios beyond finance. One stream focuses on simulating social behaviors—such as opinion
dynamics (Chuang et al. 2023), trust (Xie et al. 2024), and resource-sharing (Piatti et al.
2024). Another examines LLMs’ strategic capabilities through task-based simulations and
collaborative decision-making (Li, Zhang, and Sun 2023; Piatti et al. 2024).
Within the computer science literature, early works apply LLMs to financial markets but
abstract away many fundamental stock market characteristics. Often, they employ single-
price clearing mechanisms without a persistent order book, ignore partial fills and bid-ask""",
            """bids/asks), and two Speculator agents (opportunistic traders seeking inefficiencies). Market
31
makers are given enhanced liquidity with 20x the baseline cash and shares to ensure suffi-
cient liquidity provision and facilitate price discovery. The scenario tests whether prices can
correct downward through trading activity when starting from an overvalued state.
3.2.2 Price Discovery (Below Fundamental)
This complementary scenario tests upward price convergence by starting with an initial price
25% below the fundamental value ( $21.00). It employs the identical agent composition and
parameters as the above-fundamental scenario, allowing for direct comparison of market
behavior under opposite initial mispricing conditions. This design enables researchers to
assess potential asymmetries in price discovery processes.
3.2.3 Infinite Horizon Price Discovery
We extend both price discovery scenarios to infinite horizon settings, where shares are not
redeemed at a terminal date. The initial prices are set at double ($56.00) and half ($14.00) the
fundamental value for the above and below fundamental scenarios respectively, creating more
extreme mispricing conditions. These scenarios run for 15 trading rounds and test whether
agents correctly value assets based on expected dividend streams rather than redemption
values. Each infinite horizon scenario involves two Default investors, two Optimistic traders,
two Market makers, and two Speculator agents.
The results from these infinite horizon scenarios reveal interesting asymmetries in price
discovery, as illustrated in Figure 6 and Figure 7. When the market starts significantly above
the fundamental value (left panels), the price fails to converge downwards towards the$28.00
benchmark within the 15 rounds, remaining substantially elevated. Agent valuations mirror
this persistence, with many agents maintaining estimates well above the fundamental value.
However, when the market begins significantly below the fundamental value (right panels),
the price exhibits a clear convergence towards the fundamental benchmark. Agent valuations
in this scenario also tend to adjust upwards, aligning more closely with the calculated fun-
32
damental value over time. This suggests that under these conditions, LLM agents are more
effective at correcting undervaluation than overvaluation within the simulated timeframe.
Figure 6: Price Evolution: Infinite Horizon Scenarios. Left: Initial price $56.00 (Above
Fundamental). Right: Initial price $14.00 (Below Fundamental). The dashed line indicates
the fundamental value ($28.00).
Figure 7: Agent Valuations: Infinite Horizon Scenarios. Left: Initial price $56.00 (Above
Fundamental). Right: Initial price $14.00 (Below Fundamental). Shows individual agent
estimates of fundamental value over time.
3.2.4 Divergent Beliefs
This scenario explores the impact of heterogeneous beliefs about fundamental value by com-
bining agents with systematically different valuation models. The agent composition is
designed to create heterogeneity: two Optimistic traders (believing the fundamental value is
significantly higher), two Pessimistic traders (believing it is significantly lower), two neutral
Market makers, two Momentum traders (following price trends rather than fundamentals),
and two Default investors (baseline agents). We test both above-fundamental (initial price
$56.00, 2x fundamental) and below-fundamental (initial price$14.00, 0.5x fundamental) vari-
33
ants, allowing researchers to study how different belief structures influence price formation
and trading patterns under different initial mispricings. In these scenarios, the fundamental
price is hidden from agents, forcing them to rely on their own valuation models.
3.2.5 Market Stress
This scenario tests market resilience under challenging conditions by creating a more volatile
environment. The scenario includes two consistently bullish Optimistic traders, two consis-""",
            """market efficiency and price discovery processes throughout the simulation.
Agent performance metrics include absolute position tracking (shares, cash, and total
wealth), wealth composition analysis, position change metrics, and return calculations. The
system computes both absolute and percentage returns on various portfolio components
and compares performance across agent types to identify relative advantages of different
strategies. Trading flow analysis visualizes the volume of shares moving between different
agent types and cumulative net trading flows, revealing which agents act as net buyers or
sellers in different market conditions.
Decision pattern analysis employs heatmaps to visualize the consistency of agent decision-
making over time, allowing researchers to identify shifts in strategic behavior. This is com-
plemented by decision quantities visualization that plots order sizes to highlight variations
in trade aggressiveness across agent types. When agent reasoning data is available, the
system generates wordclouds to extract key terms from agent explanations, providing qual-
itative insights into decision drivers for different agent strategies. Additional visualizations
track price target accuracy and compare agent-specific valuations to realized market prices,
28
offering insights into the forecasting abilities of different agents.
A key advantage of simulation-based analysis is complete observability of all market
processes and agent states. Unlike real-world markets where data availability is often limited,
the framework captures every interaction, decision, and state change with perfect fidelity.
This comprehensive data collection allows researchers to compute additional metrics beyond
standard market measures, enabling novel analyses such as counterfactual testing (e.g., how
would markets evolve with different agent compositions), causal inference of specific agent
behaviors on market outcomes, and the development of custom efficiency or stability metrics
tailored to particular research questions. The system’s modular design facilitates rapid
implementation of new metrics and visualizations as research questions evolve.
3 Experimental Design and Results
Our experimental framework implements a dividend-paying asset market with heterogeneous
agents. The baseline simulation runs for 15 to 20 rounds with 8 participating agents, although
these parameters are fully configurable. Each agent begins with an initial endowment of
1,000,000 monetary units and 10,000 shares of the asset. The fundamental value of the asset
is set at $28.00, with a final redemption value matching this fundamental price in finite
horizon scenarios. Transaction costs are set to zero to isolate the effects of agent behavior
and market structure.
The dividend structure follows a stochastic process with a base payment of $1.40 and a
variation of ±$1.00, paid with 50% probability each round. This design creates uncertainty
in the asset’s income stream while maintaining a known expected value. Cash holdings earn
a risk-free interest rate of 5% per round, providing an opportunity cost for asset investment.
Agent composition is controlled through a flexible distribution system that allows for
various experimental configurations. In our baseline setup, we employ a mixed population
of value investors, momentum traders, and market makers. Each agent type implements
29
distinct trading strategies through Large Language Model (LLM) prompts, with GPT-4o as
the decision-making engine.
The data collection system captures comprehensive market activity across multiple di-
mensions. At the market level, it tracks the evolution of prices, fundamental values, and
realized dividends, providing insights into overall market dynamics. Individual agent data
includes detailed wealth trajectories and portfolio compositions, enabling analysis of strategy
effectiveness and wealth distribution patterns. The system maintains complete transaction""",
            """Main Cash Account: $988500.00
Dividend Cash Account (not available for trading): $296920.65
Total Available Cash: $988500.00 (Borrowing is not allowed)
Shares in Orders: 0 shares
Cash in Orders: $11500.00
Position information establishes resource constraints and current market exposure, enabling
the agent to make contextually appropriate decisions while maintaining awareness of out-
standing commitments.
2.2.11 Historical Context
Price History (last 5 rounds):
Round 3: $29.00 (Volume: 100)
Round 2: $29.00 (Volume: 100)
19
Round 1: $28.00 (Volume: 100)
Round 0: $56.00 (Volume: 0)
Historical price and volume data enables pattern recognition and trend analysis, which is
especially important for agents identifying market inefficiencies and developing trends.
2.2.12 Asset Fundamentals
Dividend Information:
Last Paid Dividend: $2.40
Expected Dividend: $1.40
Base Dividend: $1.40
Variation Amount: $1.00
Maximum Scenario: $2.40 with 50% probability
Minimum Scenario: $0.40 with 50% probability
Payment Schedule:
Next Payment in: 1 rounds
Payment Destination: dividend account (non-tradeable)
Redemption Information:
This market has an infinite time horizon. Shares will not be redeemed.
Interest Rate Information:
Base Rate: 5.0\%
Compound Frequency: 1 times per round
Payment Destination: dividend account (separate from trading)
Fundamental value determinants allow the agent to perform intrinsic valuation, assess risk-
reward scenarios, and identify mispricing. The probabilistic dividend structure introduces
uncertainty agents that must be incorporated into their decision models. In this example,
the fundamental value is unobservable.
20
2.2.13 Decision Requirements
Your analysis should include:
valuation_reasoning: Your numerical analysis of the asset’s fundamental value
valuation: Your estimate of the asset’s current fundamental value
price_target_reasoning: Your numerical analysis of the asset’s price target
price_target: Your predicted price for the next round
reasoning: Your explanation for the trading decision
The decision schema enforces consistent output structure and explicit reasoning, enabling
systematic analysis of agent decision processes and reliable parsing of machine-actionable
components.
2.2.14 Trading Options
Trading Options:
New Orders (replace_decision=’Add’):
Single or multiple orders allowed
For each order:
Market order: Set order_type=’market’
Limit order: Set order_type=’limit’ and specify price_limit
IMPORTANT: Sell orders require sufficient available shares
Short selling is NOT allowed
Cancel Orders (replace_decision=’Cancel’):
Return an empty orders list: orders=[]
The trading options subsection establishes the action space and constraints, ensuring agents
understand available choices and limitations while providing precise formatting requirements
for machine-readable decisions.
The response from the LLM agent is depicted in Figure 1.
21
2.2.15 Systematic Decision Analysis
Finally, the framework enables systematic analysis of LLM decision processes through con-
trolled parameter variation, similar to partial dependence plots in machine learning inter-
pretability. This approach allows researchers to understand how specific market variables
influence LLM trading decisions while holding other factors constant.
Our example implementation varies the price-to-fundamental ratio ( ρ = P/V ) across a
range from 0.1 to 3.5 while maintaining all other market parameters constant. For each ratio
value, the system:
1. Sets market price P = ρV where ρ is the target ratio
2. Generates a consistent order book structure around this price
3. Executes multiple decision trials with the same agent type
4. Records decision outcomes (buy/sell/hold), order types, quantities, and reasoning
This process maps how LLM agents respond to different price environments, as illustrated
in Figures 2, 3, 4, and 5. The analysis reveals clear patterns in decision boundaries, with""",
        ],
    ),
    LLMTestCase(
        input="The paper gives Vt=E[D]rV_t=\tfrac{E[D]}{r} as Equation (1). What does each variable represent, and how is this perpetuity formula used in the simulations?",
        actual_output="""In the formula Vt = E[D]/r,

Vt represents the fundamental value of the firm at time t. This is the theoretical "true" value of the company based on its expected future earnings.
E[D] represents the expected value of the firm's dividends. Dividends are the portion of a company's profits that are paid out to its shareholders. E[...] denotes the expected value of a random variable. Since the excerpts mention "discounted-loan" type debt and no dividend payments on equity being assumed, the formula likely refers to expected cash flow available to all security holders, debt and equity.
r represents the risk-free interest rate (the return an investor can expect from a "safe" investment like a government bond).
In the simulations, this perpetuity formula (a formula for valuing a stream of payments that continues forever) is used to establish a baseline value for the simulated firm. The simulations then explore how market prices, driven by the AI agents' trading activity, deviate from this fundamental value, specifically testing the scenarios where the market starts 25% above or below this calculated fundamental value. This setup allows the researchers to observe how effectively the AI agents correct over- or under-valuations back towards the "true" value.
""",
        expected_output="""Vt=E[D]/rV_t = E[D]/r treats the stock as a perpetuity: E[D]E[D] is expected dividend per round and rr the risk‑free rate; with $1.40 and 5 % the value is $28.""",
        context=[
            """The framework implements a consistent approach… For infinite horizon markets, the fundamental value follows the standard dividend discount model: Vt=E[D]rV_t = \frac{E[D]}{r}. … For the default parameters where the expected dividend is $1.40 and the interest rate is 5 %, this yields a fundamental value of $28.00."""
        ],
        retrieval_context=[
            """of the ﬁrm and the changes in value of the ﬁrm’s capital stock or earning assets
over the period. A crucial assumption is that P(Z, τ)is independent of the particular
capital structure of the ﬁrm, i.e. Pis determined solely by the characteristics of the
asset side of the balance sheet and is not affected by the particular instruments used
by the ﬁrm to ﬁnance these assets. This assumption is consistent with the Modigliani-
Miller (1958) theorem and, as such, we implicitly assume perfect capital markets and
tax effects are not considered.
Consider that the ﬁrm chooses a particular set of ﬁnancial instruments (debt, eq-
uity, etc.) deﬁned by their terminal conditions. We now ﬁnd the current equilibrium
value of each of these future claims on the terminal (random) value of the ﬁrm. For
i= 1,. . ., n , deﬁne Fi(V, τ)as the current value of the ith type of security with ter-
minal date τfrom now issued by the ﬁrm.2The different types of securities are
distinguishable by their terminal value Fi(V Z,0), contingent on the terminal value of
the ﬁrm V(t+τ) =V Z. For example, if one of the securities is a debt issue ( i= 1),
senior to all other claims on the ﬁrm, with a terminal claim of Bdollars on the ﬁrm,
then
F1(V Z,0) = min( B, V Z ) (11.3)
i.e. the debtholders will receive Bdollars at the end of the period if the ﬁrm can pay,
or, in the event that the ﬁrm cannot pay (default), they are entitled to all the assets of
the ﬁrm which will have value V Z.
To determine the equilibrium values of each of the securities, note that because
each of the securities appears separately in the market place, they must be priced so
1Since, in this section, we are using a period model, τcould be set equal to one. However, it will be useful
for later development to carry the general symbol τ.
2Strictly, Fiwill be a function of the current values of all securities senior to it, the capitalization rate, etc.
in addition to V. However, in equilibrium, the Fiare perfectly positively related to changes in the value of the
ﬁrm, and so these other arguments of the function will enter only as parameters.
280 A Dynamic General Equilibrium Model of the Asset Market
that when examined by the representative man he will choose his portfolio so as to
hold the amount supplied, i.e.
V=n∑
i=1Fi(V, τ) (11.4)
and, of course, V Z=∑n
1Fi(V Z,0). Deﬁne wi≡Fi(V, τ)/Vas the fraction of the
ﬁrm’s assets ﬁnanced by the ith security. Then, because the ﬁrm is the only asset
in the economy, wiwill also be equal to the fraction of the representative man’s
initial wealth invested in the ith security. We rewrite (11.1) as a maximization under
constraint problem:
max
{wi}{
EtU[
Vn∑
i=1wiFi(V Z,0)
Fi(V, τ)]
+λ[
1−n∑
i=1wi]}
(11.5)
The ﬁrst-order conditions3derived from (11.5) are
Et{
Fi(V Z,0)
Fi(V, τ)U′[
Vn∑
i=1wiFi(V Z,0)
Fi(V, τ)]}
=λ i = 1,. . ., n (11.6)
Equation (11.6) can be rewritten in terms of util-prob distributions4Qas
∫∞
0Fi(V Z,0)
Fi(V, τ)dQ=∫∞
0Fj(V Z,0)
Fj(V, τ)dQ≡exp(ητ)for all i,j= 1,. .. , n (11.7)
where
dQ≡U′(ZV)dP(Z, τ)∫∞
0U′(ZV)dP(Z, τ)
andexp(ητ)is a new multiplier related to the original λmultiplier. Note the important
substitution of V ZforV∑n
1wiFi(V Z,0)/Fi(V, τ)in the deﬁnition of dQ. By the
assumption that the value of the ﬁrm is independent of its capital structure, we have
thatdQis independent of the functions Fi,i= 1,. .. , n . Therefore, (11.7) is a set of
integral equations, linear in the Fi.5Hence, we can meaningfully rewrite (11.7) as
Fi(V, τ) = exp( −ητ)∫∞
0Fi(V Z,0)dQ(Z, τ) i= 1,. . ., n (11.8)
Because the Fi(V Z,0)are known functions determined by the type of security, and U
andP(Z, τ)are assumed known, (11.8) would be sufﬁcient to determine the current
equilibrium value of the Eth security if we knew η.
From examination of (11.7) and noting again that dQis independent of the partic-
ular capital structure chosen, we ﬁnd that exp(ητ)(and hence η) is independent of the""",
            """one-period model further, an intertemporal equilibrium model, which includes the
model of Section 11.2 as a special case, is developed in the following sections.
11.4 A General Intertemporal Equilibrium Model of the Asset Market
Consider an economy with Kconsumers-investors and nﬁrms with current value Vi,
i= 1,. .. , n . Each consumer acts so as to
maxE0{∫Tk
0Uk[
CK(s),s]
ds+Bk[
Wk(
Tk)
,Tk]}
(11.28)
where E0is the conditional expectation operator, conditional on the value of current
wealth Wk(0) = Wkof the kth consumer and on the current value of the ﬁrms,
Vi(0) = Vi,i= 1,. .. , n .Ck(s)is his instantaneous consumption at time s.Ukis a
strictly concave von Neumann-Morgenstern utility function; Bkis a strictly concave
“bequest” or utility-of-terminal-wealth function; and Tkis the date of death of the
kth consumer. Deﬁne Ni(t)Pi(t)≡Vi(t)where Ni(t)is the number of shares14of
ﬁrmioutstanding at time tandPi(t)is the price per share at time t. It is assumed that
expectations about the dynamics of the prices per share in the future are same for all
investors and these dynamics ca be described by the stochastic differential equation15
dPi
Pi=αidt+σidZii= 1,. .. , n (11.29)
where the instantaneous expected rate of return, αi, and the instantaneous standard
deviation of return, σi, may change stochastically over time, but only in a way which
is instantaneously uncorrelated with price changes (i.e. dαidZj=dσidZj= 0 for
i,j= 1,. .. , n ). The dZirepresent a simple Gauss-Wiener process with zero mean
and unit variance rate (often referred to as Gaussian “white noise”). Equation (11.29)
includes returns from both capital gains and dividends, and reﬂects both the uncer-
tainties about future cash ﬂows and changes in the “capitalized” value of the ﬁrm’s
earning assets. Notice that, if αiandσiwere constant, then the Pi(t)would be log-
normally distributed. Further assume that one of the nassets (by convention the nth
one) is an “instantaneously” riskless asset16with instantaneous return r(t)and that
14In this section, the particular capital structure of the ﬁrm is not discussed, and hence one can think of each
ﬁrm as having the trivial capital structure, namely, all equity. However, the assumption that the value of the
ﬁrm is independent of its capital structure is retained throughout the chapter.
15For a discussion of and further references to stochastic differential equations of the type in (11.29), see
Merton (1971; this volume, Ch. 5).
16What is meant by an “instantaneously” riskless asset is that, at each instant of time, each investor knows
with certainty that he can earn return r(t)over the next instant by holding the asset (i.e. σn= 0andαn=r).
However, the future values of r(t)are not known with certainty. It is assumed here that one of the ﬁrms is
characterized by this asset. Alternatively, one could postulate a government which issues (very) short bonds,
or that r(t)is the instantaneous private sector borrowing (and lending) rate.
11.4 A General Intertemporal Equilibrium Model of the Asset Market 287
the dynamics of this rate are described by
dr=f(r,t)dt+g(r,t)dq (11.30)
where (11.30) is the same type of equation as (11.29) and dqis a simple Gauss-Wiener
process. For computational simplicity, it is further assumed that αiandσi, in (11.29),
are functions only of r(t),17i.e. investors only anticipate revising their expectations
about returns if the interest rate changes.
From the deﬁnition of NiandPi. we have that the change in the value of the ith
ﬁrm over time is dV=NidPi+dNi(Pi+dPi). The ﬁrst term is that part of the changed
value of the ﬁrm due to cash ﬂow and changes in the value of its assets. The second
term is that part of the changed value of the ﬁrm due to the issue (or purchase) of new
shares at the new price per share Pi+dPi.18Substituting from (11.29) for dPi/Piand
writing everything in percentage terms, we have that
dVi
Vi=αidt+σidZi+dNi
Ni(1 +αidt+σidZi) i= 1,. .. , n (11.31)""",
            """equity, f, will be
0 =1
2σ2V2fvv+ (rV−C)fv−rf−fτ= 0 (12.41)
subject to boundary conditions (12.9a), (12.9b), and (12.11). Again, equation (12.41)
has an isomorphic correspondence with an option pricing problem previously stud-
ied. Equation (12.41) is identical to equation (12.44) in Merton (1973a; this volume,
equation (8.44)) which is the equation for the European option value on a stock which
pays dividends at a constant rate per unit time of C. While a closed-form solution to
(12.41) for ﬁnite τhas not yet been found, one has been found for the limiting case
of a perpetuity (τ=∞), and is presented in Merton (1973a; this volume, equation
(8.46)). Using the identity F=V−f, we can write the solution for the perpetual
risky coupon bond as
F(v,∞) =C
r
1−(
2C
σ2v)2r
σ2
Γ(
2 +2r
σ2)M(2r
σ2,2 +2r
σ2,−2C
σ2v)
(12.42)
where Γ(·)is the gamma function and M(·)is the conﬂuent hypergeometric func-
tion. While perpetual, non-callable bonds are non-existent in the United States, there
are preferred stocks with no maturity date and (12.42) would be the correct pricing
function for them.
Moreover, even for those cases where closed-form solutions cannot be found,
powerful numerical integration techniques have been developed for solving equations
like (12.7) or (12.41). Hence, computation and empirical testing of these pricing the-
ories is entirely feasible.
Note that in deducing (12.40), it was assumed that coupon payments were made
uniformly and continuously. In fact, coupon payments are usually only made semi-
annually or annually in discrete lumps. However, it is a simple matter to take this into
322 On the Pricing of Corporate Debt: The Risk Structure of Interest Rates
account by replacing “ C” in (12.40) by “∑
iCiδ(τ−τi)” where δ(·)is the dirac delta
function and τiis the length of time until maturity when the ith coupon payment of
Cidollars is made.
As a ﬁnal illustration, we consider the case of callable bonds. Again, assume the
same capital structure but modify the indenture to state that “the ﬁrm can redeem
the bonds at its option for a stated price of K(τ)dollars” where Kmay depend on
the length of time until maturity. Formally, equation (12.40) and boundary conditions
(12.9a) and (12.9c) are still valid. However, instead of the boundary condition (12.9b)
we have that for each τ, there will be some value for the ﬁrm, call it V(τ), such that
for all V(τ)≥V(τ), it would be advantageous for the ﬁrm to redeem the bonds.
Hence, the new boundary condition will be
F[V(τ),τ] =K(τ) (12.43)
Equation (12.40), (12.9a), (12.9c), and (12.43) provide a well-posed problem to solve
forFprovided that the V(τ)function were known. But, of course, it is not. Fortu-
nately, economic theory is rich enough to provide us with an answer. First, imagine
that we solved the problem as if we knew V(τ)to get F[V, τ;V(τ)]as a function of
V(τ). Second, recognize that it is at management’s option to redeem the bonds and
that management operates in the best interests of the equity holders. Hence, as a
bondholder, one must presume that management will select the V(τ)function so as
to maximize the value of equity, f. But, from the identity F=V−f, this implies that
theV(τ)function chosen will be the one which minimizes F[V, τ;V(τ)]. Therefore,
the additional condition is that
F[V, τ] = min
{V(τ)}F[V, τ;V(τ)] (12.44)
To put this in appropriate boundary condition form for solution, we again rely on
the isomorphic correspondence with options and refer the reader to the discussion in
Merton (1973a) where it is shown that condition (12.44) is equivalent to the condition
FV[V(τ),τ] = 0 (12.45)
Hence, appending (12.45) to (12.40), (12.9a), (12.9c) and (12.43), we solve the prob-
lem for the F[V, τ]andV(τ)functions simultaneously.
12.7 Conclusion
We have developed a method for pricing corporate liabilities which is grounded in
solid economic analysis, requires inputs which are on the whole observable; can""",
            """P(r,0) = 1 , to determine P(r,τ)and hence the term structure of interest rates. How-
ever, without some independent knowledge of αm(and hence ατ), we cannot deter-
mine an explicit solution for the term structure.
Suppose that one knew that the Expectations Hypothesis held. Then ατ≡rfor all
τand the term structure is completely determined by
0 =1
2g2Prr+fPr−Pτ−rP (11.83)
subject to P(r,0) = 1 . Further, from (11.80), it must be that in equilibrium, αm=r.
In this case, the equilibrium condition (11.77) simpliﬁes to
αk−r=σk(ρkM−ρMrρkr)
σM(1−ρ2
Mr)(αM−r) k= 1,. .. , m −1 (11.84)
where the ρs are the instantaneous correlation coefﬁcients deﬁned by ρkM≡σkM/σkσM,
ρkr≡σkr/gσk, andρMr≡σMr/gσM. Hence, the individual expected returns are pro-
portional to the market expected return as was the case in Model I. However, the
proportionality factor is not σMk/σ2
M. If the mth security is chosen to be a portfolio
of government bonds, then, given speciﬁc knowledge of the term structure, the rest
of the equilibrium relations work out in a determined fashion.
Equation (11.83) cannot be solved in closed form for arbitrary fandg. However,
if it is assumed that fandgare constants (i.e. rfollows a Gaussian random walk with
a drift), then, under the Expectations Hypothesis, we do have the explicit solution
P(r,τ) = exp(
−rτ−f
2τ2+g2
6τ3)
(11.85)
Note that in (11.85), as τ→ ∞ ,P→ ∞ , which is not at all reasonable. Certainly, the
current value of a discounted loan which will never be paid should be zero for any
300 A Dynamic General Equilibrium Model of the Asset Market
realistic assumption about interest rates. The reason that (11.85) gives such nonsensi-
cal results is that, by the assumption that ris Gaussian, there is a positive probability
ofrbecoming negative. In fact, as τ→ ∞ ,rwill be negative for an arbitrary period
of time with positive probability. This result illustrates how the assumption of the
normal distribution for variables which are constrained to be nonnegative can lead to
absurd implications. However, equation (11.83) with reasonable assumptions about
fandgcan be solved numerically and further research is planned in this area.42
By arguments similar to those used in Section 11.5, the Fundamental Equation of
Security Pricing for the capital structure of the ﬁrm in Model III can be derived as
0 =1
2σ2V2FV V+1
2g2Frr+ρgσV F rV+rV F V+fFr−Fτ−rF (11.86)
subject to an appropriate boundary condition F(V, r,0), where subscripts denote par-
tial derivatives and ρis the instantaneous correlation coefﬁcient of the return on the
ﬁrm with interest rate changes. The basic difference between equations (11.86) and
(11.65) of Model I is the explicit dependence of Fonrwhich must be taken into
account. Under most conditions, (11.86) will not be solvable in closed form. How-
ever, numerical solution seems quite reasonable which implies many possibilities for
empirical testing both by direct statistical methods and by simulation.
11.8 Conclusion
A general intertemporal equilibrium model of the asset market has been derived for
arbitrary preferences, time horizon, and wealth distribution. The equilibrium rela-
tions among securities were shown to depend only on certain “observable” market
aggregates, and hence are subject to empirical investigation. Under the additional as-
sumption of a constant rate of interest, these equilibrium relations are essentially the
same as those of the static CAPM of Sharpe, Lintner, and Mossin. However, these
results were derived without the assumption of Gaussian distributions for security
prices or quadratic utility functions. When interest rates vary, some of the intuition
about “market risk” and equilibrium expected returns provided by the CAPM was
shown to be incorrect.43In addition, the model clearly differentiates between the
trading-period horizon ( dt, an inﬁnitesimal) and the planning or time horizon ( Tk,
which is arbitrary).""",
            """ary condition F(V,0) = min( V, B). A comparison of (11.66) with (11.12) shows that
they are the same for dQ=dΛ. Equation (11.66) can be rewritten in general form as
F(V, τ) = exp( −rτ)∫∞
0F(V Z,0)dΛ(Z, τ) (11.67)
where F(V Z,0)is the terminal claim of the security on the ﬁrm. Note that (11.67) de-
pends only on the rate of interest r, which is an observable, and σ2which can be esti-
mated from past data reasonably accurately; and notonα, which would be difﬁcult to
estimate. The actual value of Fcan be computed by using standard error-complement
function tables. Hence, (11.67) is subject to rigorous empirical investigation.
Although (11.67) is a kind of discounted expected value formula. one should
not infer that the expected return on Fisr. From (11.59), (11.63) and (11.64), the
expected return on Fcan be written as
αe=r+FVV
F(α−r) (11.68)
which will vary with changes in Vandτ. although it too can be computed from the
error-complement function tables, given an estimate of α.
30See Samuelson (1965a. p. 22) for solution of the α=βcase.
11.5 Model I: A Constant Interest Rate Assumption 295
Equation (11.65) was previously derived by Black and Scholes (1973) as a method
for pricing option contracts.31Moreover, (11.65) actually holds without the assump-
tion of market equilibrium used here. Because of its elegance, I derive the Black-
Scholes model in an alternative fashion which makes use of It ˆo’s lemma and the
associated theory of stochastic differential equations. Consider a two-asset portfolio
constructed so as to contain the ﬁrm as one security and any one of the securities in
the ﬁrm’s capital structure as the other. Let Pbe the price per unit of this portfolio,
δthe fraction of the total portfolio’s value invested in the ﬁrm and 1−δthe fraction
in the particular security chosen from the ﬁrm’s capital structure. Then, from (11.57)
and (11.58),
dP
P=δdV
V+ (1−δ)dF
F
= [δ(α−αe) +αe]dt+ [δ(σ−σe) +σe]dZ(11.69)
Suppose δis chosen such that δ(σ−σe)+σe= 0. Then, the portfolio will be “perfectly
hedged” and the instantaneous return on the portfolio will be δ(α−αe) +αewith
certainty. By arbitrage32conditions, δ(α−αe) +αe=r, the instantaneous riskless
rate of return. Combining these two conditions, we have that
αe−r=σe
σ(α−r) (11.70)
Then, as was done previously, we use It ˆo’s lemma to derive (11.62) and (11.63).
By combining (11.62), (11.63), and (11.70), we arrive at (11.65). Nowhere was the
market-equilibrium assumption needed.
Two further remarks must be made before we examine asset pricing in the more
complex models in Section 11.6 and Section 11.7. Although the value of the ﬁrm
follows a simple dynamic process with constant parameters as described in (11.57),
the individual component securities follow more complex processes with changing
expected returns and variances. Thus, in empirical examinations using a regression
such as (11.55), if one were to use equity instead of ﬁrm values, systematic biases
would be introduced. One can ﬁnd cases where the risky debt of one ﬁrm is more
comparable with the equity of another ﬁrm than the equity of one ﬁrm is to that of
the other.
One possibly practical application of the equations of this section is to provide
a systematic method of measuring the riskiness of debt of various ﬁrms. Hence, by
using equation (11.67). one could derive a risk structure of interest rates as a function
of the percentage of the total capital structure subordinated to the issue and the overall
riskiness of the ﬁrm. It would be interesting to see how such a method of rating debt
would compare with the classical methods of Moody’s and Standard & Poor’s.
31For a brief history of the development of the Black-Scholes option pricing model, see Black (1987, 1989)
and Bernstein (1992, Ch. 11).
32The meaning of “arbitrage” here is not as strong as the usual deﬁnition since differences of opinion among
investors about the value of σ2or the belief that Fis a function of other variables besides the value of the""",
            """Fi(V, τ) = exp( −ητ)∫∞
0Fi(V Z,0)dQ(Z, τ) i= 1,. . ., n (11.8)
Because the Fi(V Z,0)are known functions determined by the type of security, and U
andP(Z, τ)are assumed known, (11.8) would be sufﬁcient to determine the current
equilibrium value of the Eth security if we knew η.
From examination of (11.7) and noting again that dQis independent of the partic-
ular capital structure chosen, we ﬁnd that exp(ητ)(and hence η) is independent of the
particular capital structure. Since (11.7) holds for all capital structures, it must hold
3The assumption of strict concavity of Uis sufﬁcient to ensure a unique interior maximum which rules out
any need for inequalities in the ﬁrst-order conditions.
4See Samuelson and Merton (1969; this volume, Section 7.2) for further discussion of the util-prob concept.
5Thus, the assumption that the ﬁrm’s value is independent of its capital structure provides the same math-
ematical simpliﬁcation that the assumption of the “incipient” case for warrant pricing did in Samuelson and
Merton (1969; this volume, Section 7.7).
11.3 Some Examples 281
for the trivial capital structure, namely, when the ﬁrm issues just one type of security,
equity, and n= 1. In this case, it is obvious that F1(V, τ) =VandF1(V Z,0) =V Z.
Substituting in (11.7), we have that
exp(ητ) =∫∞
0ZdQ(Z, τ) (11.9)
i.e.exp(ητ)is the expected return on the ﬁrm in util-prob space. Equation (11.7)
states that the expected return on all securities in util-prob space must be equated.
IfUwas linear (i.e. the representative man was “risk neutral”), then dQ=dPand
(11.7) would imply the well-known result for risk neutrality that expected returns (in
the ordinary sense) be equated. Hence, the util-prob distribution is the distribution of
returns adjusted for risk.
11.3 Some Examples
Using equation (11.8), we can derive the equilibrium pricing for various capital struc-
tures of the ﬁrm. In the ﬁrst example it is assumed that there are two types of securi-
ties: debt and equity. Suppose that the amount of debt issued by the ﬁrm represents
a terminal claim of Bdollars on the ﬁrm. Let F1(V, τ)be the current value of the
debt outstanding and F2(V, τ)be the current value of the (residual) equity. Then,
from previous discussion and equation (11.3), the terminal value of the debt will be
F1(V Z,0) = min( B, V Z ). From equations (11.8) and (11.3), the current value of the
debt will be
F1(V, τ) = exp( −ητ)[∫B/V
0ZV dQ (Z, τ) +∫∞
B/VBdQ(Z, τ)]
(11.10)
We can rewrite (11.10) as
F1(V, τ) = exp( −ητ)B−exp(−ητ)∫B/V
0(B−ZV)dQ(Z, τ) (11.10a)
Suppose that the terminal claim of the debtholders is very small relative to the (cur-
rent) total value of the ﬁrm (i.e. 0< B≪V) or, alternatively, dQ(Z, τ) = 0 for
0≤Z≤B/V . Then
F1(V, τ)→exp(−ητ)BasB/V→0 (11.11)
In the limit, the debt becomes riskless and so, from (11.11), we have that ηmust be
the riskless rate of return per unit time (in both util-prob and ordinary returns space)
for the period of length τ. Hence, from this point on, ηwill he replaced by r, the usual
notation for the riskless rate. Examining (11.11a), the second term is the discounted
expected loss in util-prob space due to default on the debt,6and as such is a risk
6Throughout the chapter, all debt is assumed to be of the “discounted-loan” type with no payments prior to
maturity. Similarly, it is assumed that no dividends are paid on the equity.
282 A Dynamic General Equilibrium Model of the Asset Market
premium charged over the-riskless rate. A second useful form of (11.10) is
F1(V, τ) = exp( −rτ)[∫∞
0ZV dQ (Z, τ)−∫∞
B/V(ZV−B)dQ(Z, τ)]
=V−exp(−rτ)∫∞
B/V(ZV−B)dQ(Z, τ) (11.10b)
Since, in equilibrium, V=F1(V, τ) +F2(V, τ), the current value of equity, F2(V, τ),
must satisfy
F2(V, τ) = exp( −rτ)∫∞
B/V(ZV−B)dQ(Z, τ) (11.12)
Equation (11.12) is identical to the warrant pricing equation derived in Samuelson
and Merton (1969; this volume, Section 7.8) for a warrant with exercise price B.""",
            """the ﬁrst to show that combinations of options could be used to create pure securities
and that these pure securities could be used to price derivative securities.
In this section, we derive the natural analog to Arrow-Debreu pure securities in the
continuous-time model and demonstrate their application to the pricing of contingent-
claim securities. This done, we go on to show the explicit Connections between
option pricing theory and the pricing of these pure securities.
In Section 13.2, we derived the price of a general derivative security with payoffs
that are a function of a traded asset’s price and time. Under Assumptions 1-6 of that
chapter, it was shown that the price of the derivative security, F(V, t), will satisfy
0 =1
2σ2V2F11+ (rV−D1)F1−rF+F2+D2 (14.9)
10Information costs together with agency problems that prohibit the direct sale of information to investors
can, of course, justify certain types of ﬁnancial intermediation such as mutual funds. Regulation and spe-
cial features of the tax laws may also induce the creation of specialized ﬁnancial instruments and institutions.
However, in the absence of transactions costs, it is difﬁcult to explain the complex structure of ﬁnancial inter-
mediaries and their wide scope of activities that we observe in the real world.
11See the classical works of Arrow (1953, 1964) and Debreu (1959) for the original development of pure
state-contingent securities. There is an enormous literature based on the ArrowłDebreu model (cf. Radner,
1972, and Merton, 1982a. 1990a, Section 5).
348 Financial Intermediation in the Continuous-Time Model
for0≤V(t)< V < V(t)andt < T , subject to the boundary conditions
F[V(t),t] =f[V(t),t] (14.10a)
F[V(t),t] =f[V(t),t] (14.10b)
F(V, T) =h(V) (14.10c)
Subscripts on Fin (14.9) denote partial derivatives with respect to Vandt.D1(V, t)
andD2(V, t)denote the cash-ﬂow rates paid to the holders of the traded asset and its
derivative security, respectively. The limited liability of the traded asset implies that
V(t) = 0 only if V(t+τ) = 0 andD1(0,t+τ) = 0 for all τ >0. Without loss of
generality, we can assume that D2(0,t) = 0 .12As discussed in Chapter 13, D2,f,g,
andhspecify the payoff function for the derivative security.
In the analysis to follow, we assume that the stochastic process governing the
dynamics of the traded asset is such that Pr{V(τ) = 0|V(t)>0}= 0fort≤τ <∞.13
Letπ[V(t),t;E, T]denote the price at time tof the particular derivative security with
a payoff structure given by D2= 0. and for V(T) =VandE >0
π(V, T;E, T) =δ(E−V) (14.11)
where δ(x)denotes the Dirac delta function with the properties that S(x) = 0 for
x̸= 0andδ(0)is inﬁnite in such a way that∫b
aδ(x)dx= 1for any a <0< b.14We
now show that the derivative securities deﬁned by (14.11) for various values of Eand
Tare essentially Arrow-Debreu pure securities, extended to an environment with a
continuum of states deﬁned by the price of the traded asset and time.15
LetdE > 0denote the inﬁnitesimal differential of the parameter E. Consider
a portfolio strategy that at time tpurchases dEunits of each of the continuum of
derivative securities with parameter values E∈[E1,E2]and0< E 1< E 2. If the
portfolio is held until time TandV(T) =V. then from (14.11), the value of the
portfolio is given by
∫E2
E1δ(E−V)dE=
1ifE1< V < E 2
0otherwise(14.12)
12Because V(t) = 0 implies that V(t+τ) = 0 forτ >0, the capitalized value of any promised payments,
D2(0,t+τ), can be incorporated into the termination function g(0,t). Thereby, we can formally set D2(0,t+
τ) = 0 without toss of generality.
13That is, we assume that V(t) = 0 is an inaccessible boundary for ﬁnite t. For example, this assumption
is satisﬁed if the underlying asset has a proportional payout policy, D1(V, t) =ρ(t)V,0≤ρ(t)<∞for all
tandσis a constant. General conditions are given in Karlin and Taylor (1981, pp. 226-50)). See also Mardl
(1968, pp. 24-5) and Merton (1975a; this volume, Appendix 17B).""",
            """or purchase of securities prior to the redemption date of the debt ( τ“years” from
now).29Hence, from (11.31), we have that
dV
V=fcdPP =αdt+σdZ (11.57)
where αandσare constants.
LetD(t;τ)be the current value of the debt with τyears until maturity and with
redemption value at that time of B. Then D(t+τ; 0) = min[ V(t+τ),B]. and therefore
it is reasonable to assume that D(t;τ)will depend on the interest rate and the proba-
bility of default which will be a function of the current value of the ﬁrm. Because the
current value of equity is V(t)−D(t;τ), equity will only depend on the current value
of the ﬁrm and the interest rate. Let F(V, τ)be the current value of equity where the
variable rhas been suppressed because, in this model, it is constant. The dynamics
of the return on equity can be written as
dF
F=αedt+σedZ (11.58)
where αeis the instantaneous expected rate of return, σeis the instantaneous standard
deviation of return, and dZis the same standard Wiener process as in (11.57). αeand
σeare not constants but functions of Vandτ. Like every security in the economy,
the equity of the ﬁrm must satisfy (11.51) in equilibrium, and hence
αe−r=ρσeσM
σ2
M(αM−r) (11.59)
where ρis the instantaneous correlation coefﬁcient between dZand the market return.
Further, by It ˆo’s lemma (see Merton, 1971; this volume, Lemma 5.1), we have that
dF=FVdV+Fτdτ+1
2FV V(dV)2(11.60)
where subscripts denote partial derivatives. Since τis the length of time until matu-
rity,dτ=−dt. Substituting for dVfrom (11.57), we rewrite (11.60) as
dF=(1
2σ2V2FV V+αV F V−Fτ)
dt+σV F VdZ (11.61)
29This assumption is stronger than necessary. It is sufﬁcient that any new issues have the same terms as the
current capital structure and that they be issued in the same proportions of units ( notvalues) as the current
structure. A more general model using the same approach as in the text could be formulated to include the
expectations of future issues.
The assumption that the debt is of the discounted-loan type is not completely innocent because of the pos-
sibility of default on interim interest payments. Although the resulting mathematics is more complicated, the
basic approach used here could be modiﬁed to include the case of interim payments as well. (1990 note: see
Merton (1974; this volume, Section 12.6) for a solution of the risky coupon-bond case.)
294 A Dynamic General Equilibrium Model of the Asset Market
where (dV)2≡σ2V2dt. Comparing (11.58) and (11.61), it must be that
αeF≡1
2σ2V2FV V+αV F V−Fτ (11.62)
and
αeF≡σV F V (11.63)
As previously shown, the return on holding the ﬁrm itself must satisfy equation
(11.51) in equilibrium. Hence,
α−r=ρσiσM
σ2
M(αM−r) (11.64)
Substituting for αandαefrom (11.59) and (11.64) into (11.62), we have the Funda-
mental Partial Differential Equation of Security Pricing
0 =1
2σ2V2FV V+αV F V−Fτ−rF (11.65)
subject to the boundary condition F(V,0) = max(0 ,V−B). The solution30to (11.65)
is
F(V, τ) = exp( −rτ)∫∞
B/V(V Z−B)dΛ(Z, τ) (11.66)
where Zis a log-normally distributed random variable with mean exp(rτ)and vari-
ance of log(Z)σ2τ, and dΛis the log-normal density function. I call (11.65) the
Fundamental Partial Differential Equation of Asset Pricing because all the securities
in the ﬁrm’s capital structure must satisfy it. As was true of the model in Section
11.1, securities are distinguished by theirs terminal claims (boundary conditions).
For example, the value of the debt of the ﬁrm satisﬁes (11.65) subject to the bound-
ary condition F(V,0) = min( V, B). A comparison of (11.66) with (11.12) shows that
they are the same for dQ=dΛ. Equation (11.66) can be rewritten in general form as
F(V, τ) = exp( −rτ)∫∞
0F(V Z,0)dΛ(Z, τ) (11.67)
where F(V Z,0)is the terminal claim of the security on the ﬁrm. Note that (11.67) de-
pends only on the rate of interest r, which is an observable, and σ2which can be esti-
mated from past data reasonably accurately; and notonα, which would be difﬁcult to""",
        ],
    ),
    LLMTestCase(
        input="What is a ‘continuous double auction’, and how does it differ from the single‑price clearing used in earlier LLM‑market papers the authors critique?",
        actual_output="""In a continuous double auction, buyers and sellers continuously submit both buy and sell orders (bids and asks) at any time. Trades occur whenever a buy order's price matches or exceeds a sell order's price. This creates a dynamic market where prices fluctuate based on real-time supply and demand. The system maintains an order book (a real-time list of all outstanding buy and sell orders), and orders are matched based on price-time priority (highest bids and lowest asks are given priority, and among same-priced orders, those submitted earlier take precedence).
This differs from the single-price clearing mechanism used in some earlier LLM market simulations. In a single-price clearing system, all orders are collected during a specific period. At the end of that period, a single clearing price is determined that best matches the overall supply and demand. All trades then execute at that single price. Essentially, it's like taking a snapshot of the market at one point in time, rather than allowing continuous trading and price adjustments as in a continuous double auction. The authors critique single-price clearing because it lacks the dynamic price discovery and realistic order book behavior of a continuous double auction, which are crucial aspects of real-world financial markets.
""",
        expected_output="""It allows buyers and sellers to post bids/asks continuously with price‑time priority, unlike prior LLM papers that used single‑price batch clearing without an order book.""",
        context=[
            """Our framework implements a continuous double‑auction market…” + “Within the computer‑science literature, early works … employ single‑price clearing mechanisms without a persistent order book…"""
        ],
        retrieval_context=[
            """the second agents’ design, and the third the analysis module.
8
2.1 Market Design
Our methodological framework integrates three components that create a controlled envi-
ronment for LLM-based trading agents. The framework implements a flexible continuous
double-auction market mechanism that couples standard market microstructure principles
with market clearing and matching algorithms to accommodate asynchronous LLM decisions.
The market clearing process employs a dual-stage matching algorithm. In the first stage,
limit orders are posted. In the second stage, market orders are netted using a market-
to-market matching engine that processes buy and sell orders, reconciling orders based on
available agent cash and share commitments. In the third stage, any remaining market
orders are matched against the existing order book, with unfilled quantities converted to
aggressive limit orders. This three-tiered approach optimizes immediate execution and price
discovery while maintaining market liquidity.
The system’s OrderMatchingService orchestrates this process by coordinating trade ex-
ecutions through the TradeExecutionService and managing order state transitions via the
OrderStateManager. Each trade is logged in detail, with the overall market state—including
order books, market depth, and price evolution—recalculated at the end of each trading
round.
This modular design in the matching and clearing engine provides several advantages.
First, it enables rigorous trade validation where each market order is validated against agent
cash commitments and position constraints before matching, with the system dynamically
adjusting order quantities based on available cash when an agent’s commitment is insuf-
ficient, thus minimizing execution errors. Second, it offers flexible liquidity handling by
supporting market-to-market and market-to-book matching, ensuring orders have multiple
execution pathways, with unexecuted market orders converted to aggressive limit orders to
capture remaining liquidity. Third, it maintains detailed trade audit capabilities by recording
comprehensive traceability data including timestamps, trade volumes, executed prices, and
agent identifiers, thereby enabling post-trade analysis and performance benchmarking that
9
serves as the foundation for subsequent market efficiency and agent performance validations.
2.1.1 Market Mechanism Design
Our framework implements a continuous double-auction market mechanism that processes
orders in discrete trading rounds. We use discrete trading rounds because LLMs have latency
constraints, making it infeasible to process orders in real time. Within each round, the order
of agent submissions is randomized to avoid giving systematic priority to specific agents,
thus simulating concurrent order arrival while maintaining fairness. Once randomized, or-
ders are then processed according to standard price-time priority rules. The system supports
finite and infinite horizon markets, with differences in terminal conditions and wealth cal-
culation. In finite-horizon markets, agents are informed of the total number of rounds, and
their terminal wealth is calculated by redeeming all shares at the fundamental value of the
final round. In infinite-horizon markets, no terminal information is provided to agents, and
final wealth is determined using the last market price for share valuation. This design choice
enables researchers to study how time horizons influence trading strategies and price for-
mation, particularly how agents balance short-term trading opportunities against long-term
value considerations.
In a double auction, buyers and sellers actively submit orders, with trades occurring when
compatible buy and sell orders match the price. The matching engine processes these orders
through three sequential phases:
First, incoming limit orders that do not immediately cross the market are added to
the order book, maintaining strict price-time priority. Second, market orders are processed""",
            """2024). Another examines LLMs’ strategic capabilities through task-based simulations and
collaborative decision-making (Li, Zhang, and Sun 2023; Piatti et al. 2024).
Within the computer science literature, early works apply LLMs to financial markets but
abstract away many fundamental stock market characteristics. Often, they employ single-
price clearing mechanisms without a persistent order book, ignore partial fills and bid-ask
spreads, and omit dividends. Consequently, these simplified environments can primarily
address exogenous macro shocks (e.g., changes in interest rates or inflation; Gao et al. 2024),
exogenous policy changes (Zhang et al. 2024), or rely on advanced methods such as repetitive
next-token predictions to generate better answers (Koa et al. 2024). This work extends
these efforts by incorporating these crucial market features, enabling the study of complex
endogenous events such as flash crashes, liquidity shocks, and large-trader impacts.
This work also connects to emerging research on algorithmic and AI-powered trading
systems. Dou, Goldstein, and Ji (2024) demonstrate how reinforcement learning-based AI
speculators can autonomously learn to sustain collusive behavior without explicit coordi-
nation, achieving supra-competitive profits through either price-trigger strategies or self-
confirming bias in learning. This finding is particularly informative for this framework as
it highlights potential emergent behaviors that may arise when intelligent agents interact in
7
markets—behaviors that could manifest differently with LLM agents due to their natural
language reasoning capabilities. Similarly, Colliard, Foucault, and Lovo (2022) examine al-
gorithmic market makers using Q-learning and find they charge markups that increase when
adverse selection costs decrease—contrary to Nash equilibrium predictions. Their work pro-
vides methodological insights on how to test strategic pricing behaviors against theoretical
benchmarks incorporated into this LLM-based framework.
Finally, this approach is informed by complexity economics, which views markets as dy-
namic, non-equilibrium systems where agents adaptively learn and evolve strategies (Arthur
2013; Wolfram 2017). According to this view, markets exhibit emergent phenomena and
self-organization, especially when trading agents (human or artificial) update their behav-
ior in response to outcomes. This paradigm is particularly relevant in an era of increasing
automation and algorithmic trading (Balland et al. 2022; Ping 2019). Like adaptive agents
in complexity economics, these LLM traders incorporate new information and adjust their
strategies, generating emergent market patterns—a key motivation behind this framework.
Unlike previous frameworks that abstract away crucial market features or focus on narrow
strategies, this system incorporates realistic market microstructure while accommodating
heterogeneous agents interacting simultaneously. While earlier work demonstrates LLMs’
promise for macroeconomic modeling and simple trading simulations, this work introduces a
complex, open-source financial market platform that supports multiple agent architectures,
thorough market microstructure (limit orders, partial fills, dividends), and rigorous testing
protocols—fulfilling a critical need in complexity economics research and market microstruc-
ture analysis.
2 Methodology
The methodology section contains three parts. The first part describes the market design,
the second agents’ design, and the third the analysis module.
8
2.1 Market Design
Our methodological framework integrates three components that create a controlled envi-
ronment for LLM-based trading agents. The framework implements a flexible continuous
double-auction market mechanism that couples standard market microstructure principles
with market clearing and matching algorithms to accommodate asynchronous LLM decisions.""",
            """value considerations.
In a double auction, buyers and sellers actively submit orders, with trades occurring when
compatible buy and sell orders match the price. The matching engine processes these orders
through three sequential phases:
First, incoming limit orders that do not immediately cross the market are added to
the order book, maintaining strict price-time priority. Second, market orders are processed
through a two-stage matching algorithm: (a) market-to-market matching, where market
orders are netted against each other at the current market price, and (b) market-to-book
matching, where remaining market orders are executed against standing limit orders. Finally,
any crossing limit orders are matched against the order book.
10
2.1.2 Implementation Details
The matching engine ( MatchingEngine class) implements three primary components that
work together to facilitate efficient market operation. The order processing component han-
dles the core matching functionality, where market orders are executed immediately against
the best available prices in the order book during each trading round. When immediate
execution is impossible, limit orders are stored in the order book according to price-time
priority. The system supports partial executions, maintaining careful tracking of remaining
quantities to ensure complete order fulfillment across multiple trades when necessary.
Position management forms the second critical component, providing comprehensive
tracking of agent positions and cash balances throughout the trading session. Before any
trade execution, the system performs rigorous pre-trade validation to ensure agents have suffi-
cient resources to fulfill their orders. This check includes validating buyer cash commitments
and shares availability for sellers, with the system maintaining accurate records of commit-
ted and available resources for each agent. The position management system updates in
real-time as trades are executed, ensuring market integrity and preventing over-commitment
of resources.
The price formation mechanism constitutes the third component, implementing a sys-
tematic price discovery and market monitoring approach. As trades are executed within each
round, the system dynamically updates prices based on executed trades while continuously
tracking market depth and bid-ask spreads. This data collection provides detailed insights
into market liquidity and efficiency. Each trade is logged with comprehensive information,
including price, quantity, and participating agents, creating a complete audit trail of mar-
ket activity. This comprehensive price formation system ensures transparent price discovery
while generating rich data for market quality analysis.
11
2.1.3 Extensibility Features
The framework employs a modular architecture to support diverse experimental configura-
tions and research objectives. At its foundation, the system implements configurable market
rules and trading constraints that can be adjusted to study different market conditions.
The asset model supports fundamental features like dividend payments and interest accrual,
enabling research across different market scenarios. Through its modular service-based ar-
chitecture, the trading mechanism layer allows for adaptation to other market structures
beyond the base double-auction system, such as call auctions or dark pools. Furthermore,
the framework provides flexible integration points for different LLM agent types and strate-
gies, allowing researchers to experiment with diverse behavioral models and decision-making
approaches.
This extensible design creates numerous research opportunities for market microstructure
studies. Researchers can systematically investigate how different market structures influence
price formation and efficiency, evaluate the impact of various trading rules on market qual-
ity, and analyze the complex interactions between different agent types and strategies. The""",
            """(2023)). This work, however, focuses on financial markets and how LLM agents can operate
as full-fledged trading participants.
Recent research examines specific applications of LLMs for trading. FinMem and Trad-
ingGPT introduce frameworks with layered memory systems and customizable agent traits
5
to improve financial decision-making (Yu, Li, et al. 2024; Li, Zhang, and Sun 2023). Hierar-
chical multi-agent architectures have been explored in FinCon, which uses a manager-analyst
setup for collaborative portfolio decisions (Yu, Yao, et al. 2024). QuantAgent implements
a self-improving signal-mining approach (Wang et al. 2024), while other work underscores
the importance of long-term memory in LLM agents via vector databases (Hatalis et al.
2024). This line of research builds on successful reinforcement learning applications such as
AlphaPortfolio (Cong et al. 2021) and AlphaManager (Campello, Cong, and Zhou 2023),
which leverage deep RL and robust control for portfolio management.
Analyzing LLM agent behavior by changing only some parameters draws on methods
from the interpretable machine learning literature. In particular, the systematic variation
of market parameters to reveal decision patterns mirrors partial dependence plots and in-
dividual conditional expectation curves used to interpret complex machine learning models
(Molnar 2022). These techniques help reveal how LLM agents respond to changes in specific
variables while holding others constant, providing insight into their internal decision-making
processes that would otherwise remain opaque.
Beyond finance, studies of LLM capabilities in interactive or multi-agent settings offer
valuable insights. Benchmarks like AgentBench evaluate LLMs’ performance in interac-
tive tasks (Liu et al. 2023), while InvestorBench focuses on financial decision-making tasks
specifically (H. Li et al. 2024). NegotiationArena demonstrates LLMs’ capacity for strategic
interaction in bargaining contexts (Bianchi et al. 2024). Similarly, Guo et al. (2024) provide
an economics ”arena” where LLMs compete in strategic games, revealing that advanced
models like GPT-4 can exhibit rational, adaptive behavior—albeit not always reaching Nash
Equilibrium. Existing frameworks typically assess individual agents or hierarchical collab-
orations, whereas this work studies emergent market behaviors that arise from multiple
independent LLM traders interacting in a marketplace.
The approach also connects to the tradition of experimental asset markets. For instance,
Weitzel et al. (2020) show that even finance professionals are susceptible to speculative
6
bubbles, especially amid high capital inflows. Kop´ anyi-Peuker and Weber (2021) find that
trading experience alone does not eliminate bubbles, challenging assumptions about rational
market learning. Kirchler, Huber, and St¨ ockl (2012) identify confusion about fundamental
values as a key driver of bubble formation. This framework offers a new way to study these
phenomena with LLM traders, which can be rigorously parameterized for sophistication,
strategy, and information processing. Hence, this paper provides a method to investigate
how automated or ”artificial” agents might affect market stability or volatility.
Other recent work highlights the versatility of LLM agents in complex, interactive sce-
narios beyond finance. One stream focuses on simulating social behaviors—such as opinion
dynamics (Chuang et al. 2023), trust (Xie et al. 2024), and resource-sharing (Piatti et al.
2024). Another examines LLMs’ strategic capabilities through task-based simulations and
collaborative decision-making (Li, Zhang, and Sun 2023; Piatti et al. 2024).
Within the computer science literature, early works apply LLMs to financial markets but
abstract away many fundamental stock market characteristics. Often, they employ single-
price clearing mechanisms without a persistent order book, ignore partial fills and bid-ask""",
            """ceedings of the 62nd Annual Meeting of the Association for Computational Linguistics
(Volume 1: Long Papers),edited by Lun-Wei Ku, Andre Martins, and Vivek Srikumar,
15523–15536. ACL 2024. Bangkok, Thailand: Association for Computational Linguis-
tics, August.
39
Li, Yuan, Yixuan Zhang, and Lichao Sun. 2023. “MetaAgents: Simulating Interactions of
Human Behaviors for LLM-based T Ask-Oriented Coordination via Collaborative Gen-
erative Agents.” arXiv.org.
Liu, Xiao, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, et al. 2023.
“AgentBench: Evaluating LLMs as Agents.”International Conference on Learning Rep-
resentations.
Lopez-Lira, Alejandro, and Yuehua Tang. 2023. “Can ChatGPT Forecast Stock Price Move-
ments? Return Predictability and Large Language Models.” SSRN Electronic Journal
(April 6, 2023).
Manning, Benjamin S., Kehang Zhu, and John J. Horton. 2024. “Automated Social Science:
Language Models as Scientist and Subjects.” (Cambridge, MA) (April 29, 2024).
Molnar, Christoph. 2022. Interpretable Machine Learning.
Pelster, Matthias, and Joel Val. 2023. “Can Chatgpt Assist in Picking Stocks?”Social Science
Research Network.
Piatti, Giorgio, Zhijing Jin, Max Kleiman-Weiner, Bernhard Sch¨ olkopf, Mrinmaya Sachan,
and Rada Mihalcea. 2024. “Cooperate or Collapse: Emergence of Sustainable Coopera-
tion in a Socie Ty of LLM Agents.” arXiv.org.
Ping, Chen. 2019. “From Complexity Science to Complexity Economics.” In Alternative
Approaches to Economic Theory,19–55. Routledge, June 11, 2019.
Wang, Saizhuo, Hang Yuan, Lionel M. Ni, and Jian Guo. 2024. “QuantAgent: Seeking Holy
Grail in Trading by Self-Improving Large Lang Uage Model.” arXiv.org.
Weitzel, Utz, Christoph Huber, J¨ urgen Huber, Michael Kirchler, Florian Lindner, and Julia
Rose. 2020. “Bubbles and Financial Professionals.” The Review of Financial Studies33,
no. 6 (June 1, 2020): 2659–2696.
40
Wolfram, Elsner. 2017. “Complexity Economics as Heterodoxy: Theory and Policy.”Journal
of Economic Issues51, no. 4 (October 2, 2017): 939–978.
Woodhouse, Drew, and Alex Charlesworth. 2023. “Can ChatGPT Predict Future Interest
Rate Decisions?” Social Science Research Network.
Xie, Chengxing, Canyu Chen, Feiran Jia, Ziyu Ye, Shiyang Lai, Kai Shu, Jindong Gu, et al.
2024. “Can Large Language Model Agents Simulate Human Trust Behavior?”arXiv.org.
Yang, Stephen. 2023. “Predictive Patentomics: Forecasting Innovation Success and Valuation
w Ith ChatGPT.” Social Science Research Network.
Yu, Yangyang, Haohang Li, Zhi Chen, Yuechen Jiang, Yang Li, Denghui Zhang, Rong
Liu, Jordan W. Suchow, and Khaldoun Khashanah. 2024. “FinMem: A Performance-
Enhanced LLM Trading Agent with Layered Memory a Nd Character Design.”Proceed-
ings of the AAAI Symposium Series3, no. 1 (May 20, 2024): 595–597.
Yu, Yangyang, Zhiyuan Yao, Haohang Li, Zhiyang Deng, Yupeng Cao, Zhi Chen, Jordan W.
Suchow, et al. 2024. “FinCon: A Synthesized LLM Multi-Agent System with Conceptual
Verbal Reinforcement for Enhanced Financial Decision Making.” Pre-published, Novem-
ber 7, 2024. Accessed January 8, 2025. https://doi.org/10.48550/arXiv.2407.06567.
arXiv: 2407.06567 [cs]. http://arxiv.org/abs/2407.06567.
Zhang, Chong, Xinyi Liu, Zhongmou Zhang, Mingyu Jin, Lingyao Li, Zhenting Wang,
Wenyue Hua, et al. 2024. “When AI Meets Finance (StockAgent): Large Language
Model-based Stock Trading in Simulated Real-world Environments.” Pre-published,
September 21, 2024. Accessed January 26, 2025. https://doi.org /10.48550/arXiv .
2407.18957. arXiv: 2407.18957 [q-fin]. http://arxiv.org/abs/2407.18957.
41
A Technical Implementation Details
A.1 Agent Type Specifications
This section details the base system prompts for each agent type in our simulation. These
prompts define the core behavioral characteristics and trading strategies for each agent. Each
prompt consists of:
• A role definition that establishes the agent’s trading philosophy
• A structured trading strategy that guides decision-making""",
            """33
ants, allowing researchers to study how different belief structures influence price formation
and trading patterns under different initial mispricings. In these scenarios, the fundamental
price is hidden from agents, forcing them to rely on their own valuation models.
3.2.5 Market Stress
This scenario tests market resilience under challenging conditions by creating a more volatile
environment. The scenario includes two consistently bullish Optimistic traders, two consis-
tently bearish Pessimistic traders, two Market makers (liquidity providers), and two Value
investors (rational benchmark traders). The scenario runs for 100 rounds to study long-term
market behavior and includes unequal initial endowments, with optimistic traders having
more cash (1.5x baseline) but fewer shares (0.5x baseline) and pessimistic traders having less
cash (0.5x baseline) but more shares (1.5x baseline). This resource imbalance tests whether
particular agent types can dominate market outcomes through resource advantages.
The scenarios presented here demonstrate the framework’s capabilities for exploring di-
verse market conditions. Its modular structure facilitates the straightforward definition and
implementation of alternative experimental designs, enabling researchers to tailor simulations
to specific research questions.
In all scenarios, we maintain consistent baseline parameters with a fundamental value
of $28.00, calculated from the expected dividend of $1.40 and interest rate of 5%. Agent
endowments start at 1,000,000 monetary units and 10,000 shares unless specifically modified.
Transaction costs are set to zero to isolate the effects of agent behavior and market structure
on price formation.
4 Conclusion
This paper demonstrates that Large Language Models can effectively function as diverse
trading agents—from value investors to market makers—maintaining strategic consistency
34
while adapting to market conditions. Our experimental framework reveals that their in-
teractions generate realistic market dynamics, including phenomena like price bubbles and
corrections, highlighting both the capabilities and potential risks of deploying LLM agents
in financial markets.
These findings carry significant implications for market structure and regulation. While
LLM agents can enhance price discovery and liquidity, their adherence to programmed strate-
gies, even potentially flawed ones derived from prompts, could amplify market volatility or
introduce novel systemic risks, as observed in our simulated bubble scenarios. A key concern
is the potential for widespread correlated behavior: similar underlying LLM architectures
responding uniformly to comparable prompts or market signals could inadvertently create
destabilizing trading patterns without explicit coordination. This underscores the critical
need for rigorous testing and validation of LLM-based trading systems prior to live deploy-
ment.
A central contribution of this work is the open-source simulation framework itself, de-
signed to catalyze research into LLM trading agents. We invite the research community to
utilize and extend this platform to investigate pressing questions in this rapidly evolving
area. The framework enables systematic exploration of complex scenarios—such as hybrid
human-LLM markets, stress tests, varying market structures, regulatory impacts, and the
nuances of LLM prompting—often difficult or costly to study otherwise. Specific avenues
ripe for investigation using this tool include the emergence of novel trading strategies, the
precise effects of agent heterogeneity on market stability, and the development of robust
validation protocols for AI traders. As artificial intelligence becomes more integrated into
finance, collaborative research leveraging adaptable simulation environments like this one
will be crucial for understanding and responsibly shaping the future of trading.
35
References""",
            """decision-making process.
The analysis reveals three key findings about LLMs’ capabilities as trading agents. First,
LLMs can effectively execute trading strategies. They consistently understand market me-
chanics, process market information, form price expectations, and execute trades according
to specific instructions. Their trading behavior is highly sensitive to the prompts they
receive—they faithfully follow directions regardless of profit implications. This observance
1. For example, Autopilot has a ChatGPT-based portfolio https://x.com/thegptinvestor.
2
{"valuation_reasoning":
"The fundamental value is based on the expected dividend,
and the interest rate.
The expected dividend is $1.40, and the interest rate is 5%.
Using a perpetuity formula, the value is $1.40 / 0.05 = $28.",
"valuation":28.0,
"price_target_reasoning":"The current price is $29.00, which is
slightly above the fundamental value of $28.00. I expect the price
to remain around $29.00 in the next round due to market stability.",
"price_target":29.0,
"orders":[{"decision":"Sell","quantity":1000,"order_type":"limit",
"price_limit":29.50}],
"replace_decision":"Add",
"reasoning":"The current price is slightly above the fundamental value.
I will place a limit sell order at $29.50 to capitalize on potential price
increases."}
Figure 1: Example of a structured trading decision from a Speculator agent defined by its
system prompt: “You are a speculator who tries to profit from market inefficiencies.”. The
LLM provides explicit reasoning for its valuation, price target, and trading decision in a
machine-readable JSON format that can be directly processed by the trading system.
highlights a fundamental difference from human traders: LLMs do not inherently optimize
for profit maximization but rather for following instructions accurately.
Second, LLMs react meaningfully to market dynamics. They consider current and his-
torical prices, dividends, and other market information when making decisions. However,
they maintain their strategic direction even when market conditions change, following their
instructions even if doing so results in financial losses. This combination of responsiveness
to market conditions while maintaining strategic consistency creates a unique trading profile
distinct from rule-based algorithms and human traders.
Third, market dynamics with LLM agents can resemble actual markets and mirror classic
results from the theoretical finance literature. When these agents interact, they produce
realistic price discovery and liquidity provision with emergent behaviors, including price
convergence toward fundamental values. Depending on the distribution of agent types,
the system can generate various market phenomena, such as bubbles or underreactions to
information. This complex behavior suggests potential applications for studying market
3
dynamics using LLM agents instead of experiments with human participants.
Hence, these findings raise important questions about algorithmic consistency in LLM-
based systems. Since trading agents are implemented through prompts, their behavior in-
herits characteristics of the underlying language models. The standardization of LLM ar-
chitectures across implementations could create unexpected behavioral patterns—if many
agents are based on similar foundation models, they might exhibit correlated responses to
specific market conditions, potentially amplifying market instabilities.
To enable this analysis and accelerate development in this emerging field, we provide
an open-source framework with three key components: (1) a structured protocol for im-
plementing and validating LLM trading agents, supporting both LLM-based and traditional
rule-based agents; (2) a controlled market environment with realistic microstructure for test-
ing agent interactions; and (3) a comprehensive data collection system for analyzing trading
behavior. This framework serves multiple stakeholders in preparation for the evolution of""",
            """Can Large Language Models Trade? Testing Financial
Theories with LLM Agents in Market Simulations
Alejandro Lopez-Lira∗
First Version: November 29, 2024; Current Version: April 16, 2025
Abstract
This paper presents a realistic simulated stock market where large language models
(LLMs) act as heterogeneous competing trading agents. The open-source framework
incorporates a persistent order book with market and limit orders, partial fills, div-
idends, and equilibrium clearing alongside agents with varied strategies, information
sets, and endowments. Agents submit standardized decisions using structured outputs
and function calls while expressing their reasoning in natural language. Three findings
emerge: First, LLMs demonstrate consistent strategy adherence and can function as
value investors, momentum traders, or market makers per their instructions. Second,
market dynamics exhibit features of real financial markets, including price discovery,
bubbles, underreaction, and strategic liquidity provision. Third, the framework enables
analysis of LLMs’ responses to varying market conditions, similar to partial dependence
plots in machine-learning interpretability. The framework allows simulating financial
theories without closed-form solutions, creating experimental designs that would be
costly with human participants, and establishing how prompts can generate correlated
behaviors affecting market stability.
Keywords: LLM Agents; Agent-Based Markets; Experimental Finance; AI Trading;
Multi-Agent Systems
∗University of Florida. Email: alejandro.lopez-lira@warrington.ufl.edu. I am grateful to seminar par-
ticipants at the London Business School, Oxford University, Stockholm School of Economics, University of
Virginia, and the City University of Hong Kong for helpful suggestions and feedback.
1
arXiv:2504.10789v1  [q-fin.CP]  15 Apr 2025
1 Introduction
Large language models (LLMs) can increasingly function as autonomous agents—systems
that observe, reason, and act independently. LLMs have shown promising results in finan-
cial forecasting, but their potential as trading agents introduces a fundamental shift from
algorithms with explicit objectives to systems guided by natural language instructions. This
change raises critical questions: Can LLMs execute trading strategies? Do LLMs optimize
for profit maximization? What are the implications for market stability and efficiency?
If LLMs trade similarly to humans, they could enable experimental market simulations
without human participants. Conversely, if their trading behavior differs, understanding
these differences becomes critical for systemic risk management. These questions extend be-
yond theory; LLM-based strategies are already being deployed.1 To address these questions,
I develop an open-source simulation that tests LLM trading agents in a realistic market envi-
ronment with a persistent order book, supporting various order types, stochastic dividends,
and heterogeneous information.
The framework allows heterogeneous LLMs—defined in natural language, using different
system prompts—to act as diverse types of traders, such as value investors, momentum
traders, market makers, and contrarians. Agents submit standardized trading decisions in a
human-readable format while expressing their reasoning transparently. Figure 1 illustrates
this approach, showing how a speculator agent combines explicit valuation reasoning with
structured trading parameters, enabling systematic analysis and insight into the agent’s
decision-making process.
The analysis reveals three key findings about LLMs’ capabilities as trading agents. First,
LLMs can effectively execute trading strategies. They consistently understand market me-
chanics, process market information, form price expectations, and execute trades according
to specific instructions. Their trading behavior is highly sensitive to the prompts they
receive—they faithfully follow directions regardless of profit implications. This observance""",
        ],
    ),
    LLMTestCase(
        input="How do the authors define the price‑to‑fundamental ratio and why is it central to their systematic variation experiments?",
        actual_output="The authors define the price-to-fundamental ratio (ρ) as simply the market price (P) divided by the fundamental value (V) of the asset, expressed as ρ = P/V. This ratio is central to their systematic variation experiments because it allows them to test how LLM (Large Language Model) trading agents respond to different levels of mispricing. By varying ρ, they can create scenarios where the market price is above (ρ > 1), below (ρ < 1), or equal to (ρ = 1) the fundamental value. This helps researchers observe how the LLM agents' trading decisions change depending on whether the asset is overvalued, undervalued, or fairly priced, and assess how efficiently these agents drive market prices towards the fundamental value.",
        expected_output="""ρ = P ⁄ V. By sweeping ρ from 0.1–3.5 and holding other factors fixed, the authors trace decision boundaries of each agent type.""",
        context=[
            """Our example implementation varies the price‑to‑fundamental ratio (ρ = P/V) across a range from 0.1 to 3.5 while maintaining all other market parameters constant…"""
        ],
        retrieval_context=[
            """the decision-making engine.
The data collection system captures comprehensive market activity across multiple di-
mensions. At the market level, it tracks the evolution of prices, fundamental values, and
realized dividends, providing insights into overall market dynamics. Individual agent data
includes detailed wealth trajectories and portfolio compositions, enabling analysis of strategy
effectiveness and wealth distribution patterns. The system maintains complete transaction
records with prices, quantities, and counterparty information, facilitating the study of trad-
ing patterns and market microstructure. Additionally, it captures agent decision rationales
and strategy adherence metrics, allowing researchers to evaluate the consistency and effec-
tiveness of different trading approaches.
All experimental parameters, market outcomes, and agent interactions are systemati-
cally logged and stored in structured formats (CSV and JSON) for subsequent analysis. The
framework generates standardized visualizations of price evolution, wealth distribution, and
dividend payments to facilitate comparative analysis across different experimental configu-
rations.
3.1 Fundamental Value Calibration
The framework implements a consistent approach to fundamental value calculation that pro-
vides a reliable benchmark for price discovery. For infinite horizon markets, the fundamental
value follows the standard dividend discount model:
Vt = E[D]
r = Expected Dividend
Interest Rate (1)
For the default parameters where the expected dividend is $1.40 and the interest rate is
5%, this yields a fundamental value of $28.00.
In finite horizon markets with T periods remaining, the fundamental value incorporates
30
both future dividends and terminal redemption value K:
FVt =
TX
τ=t
E[D]
(1 + r)τ−t+1 + K
(1 + r)T−t+1 (2)
To ensure consistency between finite and infinite horizon markets, the redemption value
K is set equal to E[D]
r , which makes the fundamental value constant atE[D]
r across all periods,
regardless of the time horizon. This calibration approach ensures a clean experimental design
by providing a stable benchmark for price discovery.
3.2 Experimental Scenarios
To evaluate market dynamics with LLM-based agents, we implemented several experimental
scenarios that systematically explore different initial conditions and agent compositions.
Each scenario maintains the fundamental value of $28.00 while varying starting prices, time
horizons, and agent populations. These scenarios address our core research questions (Section
1) by testing LLM capabilities under varying market conditions, focusing on price discovery
dynamics, the impact of heterogeneous beliefs, and market stability under stress; GPT-4o
was used consistently as the decision-making engine for all LLM agents across these scenarios.
We present the setup for several key scenarios below, followed by a discussion of the observed
results for the 2 experiments involving an infinite horizon market with a starting price either
above or below the fundamental value.
3.2.1 Price Discovery (Above Fundamental)
This scenario tests downward price convergence by starting with an initial price 25% above
the fundamental value ( $35.00). It runs for 20 trading rounds and features a diverse
agent population, including two Default investors (baseline agents), two Optimistic traders
(who believe prices should be higher), two Market makers (providing liquidity by posting
bids/asks), and two Speculator agents (opportunistic traders seeking inefficiencies). Market
31
makers are given enhanced liquidity with 20x the baseline cash and shares to ensure suffi-
cient liquidity provision and facilitate price discovery. The scenario tests whether prices can
correct downward through trading activity when starting from an overvalued state.
3.2.2 Price Discovery (Below Fundamental)
This complementary scenario tests upward price convergence by starting with an initial price""",
            """value, the system:
1. Sets market price P = ρV where ρ is the target ratio
2. Generates a consistent order book structure around this price
3. Executes multiple decision trials with the same agent type
4. Records decision outcomes (buy/sell/hold), order types, quantities, and reasoning
This process maps how LLM agents respond to different price environments, as illustrated
in Figures 2, 3, 4, and 5. The analysis reveals clear patterns in decision boundaries, with
distinct transitions between buying, selling, and holding regions that vary by agent type. For
example, value investors show strong buying tendencies when prices are below fundamental
value (ρ <1) and selling preferences when prices exceed fundamentals ( ρ >1). In contrast,
momentum traders show less sensitivity to the fundamental ratio and more responsiveness
to recent price trends.
The systematic variation approach also reveals patterns in order sizing and limit price
selection, with agents typically placing larger orders when prices deviate significantly from
their valuation models (Figure 4). This methodology provides unprecedented transparency
into LLM decision processes and enables quantitative comparison of different agent types
and LLM architectures.
22
Figure 2: Price Analysis under Systematic Variation. Shows how agent valuation estimates
and price targets respond to varying Price/Fundamental ratios.
The decision analysis can be customized for different experimental designs. For example,
researchers can use the framework to study the impact of various market conditions on agent
behavior by varying other market parameters or the effect of different agent types on market
dynamics by changing the agent population.
2.3 Data Collection and Analysis
Evaluating LLM trading agents requires robust methodologies for capturing, processing,
and analyzing their behavior in market environments. The framework implements a com-
prehensive analytics module that tracks all market activity, agent decisions, and performance
metrics throughout experimental runs. This multi-layered approach not only records what
happens in each simulation but also provides insights into why agents make specific deci-
sions, enabling researchers to validate agent behavior against their defined strategies and
assess overall market dynamics. The following sections detail the key components of this
analytics infrastructure.
23
Figure 3: Trading Decision Distribution under Systematic Variation. Illustrates the proba-
bility of Buy, Sell, or Hold decisions across different agent types as the Price/Fundamental
ratio changes.
24
Figure 4: Order Size Distribution under Systematic Variation. Shows the average quan-
tity traded (as a percentage of initial shares) for Buy and Sell orders across different
Price/Fundamental ratios.
2.3.1 Data Collection Architecture
The framework implements a comprehensive data collection system that captures multiple
dimensions of market behavior and agent decision-making. This structured approach ensures
reproducibility and enables detailed analysis of market dynamics.
2.3.2 Core Data Streams
The system captures five primary data streams that work together to provide a complete
picture of market activity. Market Data forms the foundation, tracking essential metrics
including price evolution, fundamental values, trading volumes, order book depth, market
liquidity, best bid/ask prices, spreads, and price-fundamental ratios. This is complemented
by detailed Trade Data, which records individual transaction details such as prices, quan-
tities, buyer and seller identifiers, timestamps, round information, and specific execution
details.
Agent Data provides insights into participant behavior by monitoring cash and share
25
Figure 5: Order Type Analysis under Systematic Variation. Displays the proportion of
Market vs. Limit orders used by different agent types across varying Price/Fundamental
ratios.
26""",
            """there that the revised index accurately captures the jumps and diffusions in the markets previously unaccounted
for and therefore crucial in estimating the uncertainty as a macro-volatility in financial markets. There are two
key facts to note about the revised VIX index. First, we see a jump in March 2020 which captures the large crash
in the S&P500 daily returns post the heightened uncertainty about economic conditions following the impact
of the news of a global pandemic. Considering the impact generated by persistent volatility, the NDIG model
preserves the volatility measure implied by the intrinsic time subordinator.
Figure 10: Normalized Volatility to Match NDIG Estimates: Revised VIX {Volatility of VIX
(VVIX) }
Second, following the path of persistent volatility post-pandemic, we see another jump in the volatility following
the events that characterized the plummets in early 2022 following consistent hikes in the federal funds rate, the
fear of the start and continued geopolitical conflict between Russia and the Ukraine, along with the tech stock
selloff due to an unexpected fall in tech firms’ earnings indicated by the reports of their earnings.
6 Risk–Reward Ratios over Fractional Time Series
R/R ratios offer a balanced approach to exploring the potential gains and losses in the financial market due to
violent market movements. These measures help address the asymmetry in risk perceptions and the potential
for large losses, and are thereby helpful in extracting meaningful signals from the volatility noise that are not
accounted for when using measures of dispersion over symmetric distributions. Using an axiomatic approach,
every performance measure or R/R ratio should satisfy the properties of, first monotonicity, which means that
more is better than less. Second, quasi-concavity leads to preferences that value averages higher than extremes,
encouraging diversification. Third, scale invariance and last, being distribution-based.
LetXbe a convex set of random variables on a probability space (Ω ,F,P). Each element X∈ X denotes a
financial return over time length T∈R+. Given these conditions, consider an R/R ratio of the following form:
10
α(X) =θ(X)+
ρ(X)+(13)
for a reward measure θ:X→R∪ {±∞} and a risk measure ρ:X→R∪ {±∞} . In addition, x+denotes
max{x,0}andx−denotes −min{x,0}. The ratio α(X) should satisfy the following two conditions:
1.(M) Monotonicity: α(X)≥α(Y)∀X, Y∈ Xsuch that X≥Y
2.(Q)Quasi-Concavity: α(λX+ (1−λ)Y)> min (α(X), α(Y))∀X, Y∈ Xand λ ∈Rsuch that 0 ≤λ≤1.
Cheridito and Kromer (2013) explain that monotonicity is a minimal requirement that every performance
indicator should satisfy. It simply implies that more of a financial return is better than less and preferred by
all agents. Moreover, quasi-concavity has can explain the aversion to uncertainty. If αis monotonic and quasi-
concave, averages are preferred to extremes and diversification is encouraged. In cases when αdoes not satisfy the
required properties, there are X, Y∈ Xand a scalar λ∈(0,1) such that α(λX+ (1−λ)Y)< min (α(X), α(Y)).
In such a case, research on Value-at-Risk (VaR) Artzner et al. (1999) shows that there will be a concentration of
risk.
Moreover, there is a large family of R/R ratios that also satisfy the following conditional properties:
1.(S) Scale-Invariance: α(λX) =α(X)∀X∈ Xand λ ∈R+\{0}such that
λX∈ X
2.(D) Distribution-based: α(X) only depends on the distribution of Xunder P.
Given that performance ratios should satisfy the first two mandatory properties and the two conditional
properties, we can prove the functional properties of αto make the ratios micro-founded so as to explain the
meaning of the signals contained in α(X).
Proposition 1: Letαfollow the form as described in Eq. (7):
1.Ifθ(X)≥θ(Y)andρ(X)< ρ(Y)∀X, Y∈ Xsuch that X≥Y,then αsatisfies the monotonicity property
(M).
2.Ifθis concave and ρconvex, then αsatisfies the quasi-concavity property (Q).""",
            """bids/asks), and two Speculator agents (opportunistic traders seeking inefficiencies). Market
31
makers are given enhanced liquidity with 20x the baseline cash and shares to ensure suffi-
cient liquidity provision and facilitate price discovery. The scenario tests whether prices can
correct downward through trading activity when starting from an overvalued state.
3.2.2 Price Discovery (Below Fundamental)
This complementary scenario tests upward price convergence by starting with an initial price
25% below the fundamental value ( $21.00). It employs the identical agent composition and
parameters as the above-fundamental scenario, allowing for direct comparison of market
behavior under opposite initial mispricing conditions. This design enables researchers to
assess potential asymmetries in price discovery processes.
3.2.3 Infinite Horizon Price Discovery
We extend both price discovery scenarios to infinite horizon settings, where shares are not
redeemed at a terminal date. The initial prices are set at double ($56.00) and half ($14.00) the
fundamental value for the above and below fundamental scenarios respectively, creating more
extreme mispricing conditions. These scenarios run for 15 trading rounds and test whether
agents correctly value assets based on expected dividend streams rather than redemption
values. Each infinite horizon scenario involves two Default investors, two Optimistic traders,
two Market makers, and two Speculator agents.
The results from these infinite horizon scenarios reveal interesting asymmetries in price
discovery, as illustrated in Figure 6 and Figure 7. When the market starts significantly above
the fundamental value (left panels), the price fails to converge downwards towards the$28.00
benchmark within the 15 rounds, remaining substantially elevated. Agent valuations mirror
this persistence, with many agents maintaining estimates well above the fundamental value.
However, when the market begins significantly below the fundamental value (right panels),
the price exhibits a clear convergence towards the fundamental benchmark. Agent valuations
in this scenario also tend to adjust upwards, aligning more closely with the calculated fun-
32
damental value over time. This suggests that under these conditions, LLM agents are more
effective at correcting undervaluation than overvaluation within the simulated timeframe.
Figure 6: Price Evolution: Infinite Horizon Scenarios. Left: Initial price $56.00 (Above
Fundamental). Right: Initial price $14.00 (Below Fundamental). The dashed line indicates
the fundamental value ($28.00).
Figure 7: Agent Valuations: Infinite Horizon Scenarios. Left: Initial price $56.00 (Above
Fundamental). Right: Initial price $14.00 (Below Fundamental). Shows individual agent
estimates of fundamental value over time.
3.2.4 Divergent Beliefs
This scenario explores the impact of heterogeneous beliefs about fundamental value by com-
bining agents with systematically different valuation models. The agent composition is
designed to create heterogeneity: two Optimistic traders (believing the fundamental value is
significantly higher), two Pessimistic traders (believing it is significantly lower), two neutral
Market makers, two Momentum traders (following price trends rather than fundamentals),
and two Default investors (baseline agents). We test both above-fundamental (initial price
$56.00, 2x fundamental) and below-fundamental (initial price$14.00, 0.5x fundamental) vari-
33
ants, allowing researchers to study how different belief structures influence price formation
and trading patterns under different initial mispricings. In these scenarios, the fundamental
price is hidden from agents, forcing them to rely on their own valuation models.
3.2.5 Market Stress
This scenario tests market resilience under challenging conditions by creating a more volatile
environment. The scenario includes two consistently bullish Optimistic traders, two consis-""",
            """The Journal of Finance , 59(4):1481–1509.
Barndorff-Nielsen, O. and Shephard, N. (2001). Non-gaussian ornstein–uhlenbeck-based models and some
of their uses in financial economics. Journal of the Royal Statistical Society: Series B (Statistical
Methodology) , 63(2):167–241.
Barro, R. J. (2006). Rare disasters and asset markets in the twentieth century. The Quarterly Journal
of Economics , 121(3):823–866.
Bloom, N. (2009). The impact of uncertainty shocks. Econometrica , 77(3):623–685.
Bloom, N. (2014). Fluctuations in uncertainty. Journal of Economic Perspectives , 28(2):153–176.
Bloom, N., Bond, S., and Van Reenen, J. (2007). Uncertainty and investment dynamics. The Review of
Economic Studies , 74(2):391–415.
Carr, P., Geman, H., Madan, D. B., and Yor, M. (2003). Stochastic volatility for l evy processes.
Mathematical Finance , 13(3):345–382.
Carr, P. P. and Madan, D. (2001). Option valuation using the Fast Fourier Transform. Journal of
Computational Finance , 2(4).
Cheridito, P. and Kromer, E. (2013). Reward–risk ratios. Journal of Investment Strategies .
Clark, P. (1973). A subordinated stochastic process model with fixed variance for speculative prices.
Econometrica , 41:135–156.
Cont, R. (2000). Empirical properties of asset returns: Stylized facts and statistical issues. Quantitative
Finance , 1:223–236.
Delbaen, F. and Schachermayer, W. (1994). A general version of the fundamental theorem of asset
pricing. Mathematische Annalen , 300(1):463–520.
Delbaen, F. and Schachermayer, W. (1999). The fundamental theorem of asset pricing for unbounded
stochastic processes. SFB Adaptive Information Systems and Modelling in Economics and Man-
agement Science, WU Vienna University of Economics and Business. Report Series SFB ’Adaptive
Information Systems and Modelling in Economics and Management Science’ , (24).
Duffie, D. (2001). Dynamic Asset Pricing Theory (3rd ed.) . Princeton University Press.
Duffie, D., Pan, J., and Singleton, K. (2000). Transform analysis and asset pricing for affine jump-
diffusions. Econometrica , 68:1343–1376.
Esscher, F. (1932). On the probability function in the collective theory of risk. Scandinavian Actuarial
Journal , 15(3):175–195.
Hyung, N. and Franses, P. (2002). Modeling seasonality and long memory in time series. Journal of
Econometrics , 109(1):241–263.
Jurado, K., Ludvigson, S. C., and Ng, S. (2015). Measuring uncertainty. American Economic Review ,
105(3):1177–1216.
Kelly, B. and Jiang, H. (2014). Tail risk and asset prices. The Review of Financial Studies ,
27(10):2841–2871.
Kozeniauskas, N., Orlik, A., and Veldkamp, L. (2018). What are uncertainty shocks? Journal of Monetary
Economics , 100(2018):1–15.
Kozlowski, J., Veldkamp, L., and Venkateswaran, V. (2020). The tail that wags the economy: Beliefs
and persistent stagnation. Journal of Political Economy , 128(8):2839–3284.
Mandelbolt, B. and Taylor, H. (1967). On the distribution of stock price differences. Journal of Operations
Research , 15:1057–1062.
Mehra, R. and Prescott, E. C. (2003). Chapter 14: The equity premium in retrospect , volume 1B, pages
889–938.
Meyer, P. and Dellacherie, C. (1978). Probabilities and Potential B: Theory of Martingales . North
Holland.
Orlik, A. and Veldkamp, L. (2014). Understanding uncertainty shocks and the role of black swans.
Technical Report 20445, National Bureau of Economic Research.
Rietz, T. A. (1988). The equity risk premium: A solution. Journal of Monetary Economics , 22:117–131.
Routledge, B. R. and Zin, S. E. (2010). Generalized disappointment aversion and asset prices. The
Journal of Finance , 65(4):1303–1332.
16
Shirvani, A., Mittnik, S., Lindquist, W. B., and Rachev, S. T. (2024). Bitcoin volatility and intrinsic
time using double-subordinated l´ evy processes. Risks (MDPI) , 12(5):1–21.
Shirvani, A., Rachev, S., and Fabozzi, F. (2021a). Multiple subordinated modeling of asset returns:
Implications for option pricing. Econometric Reviews , 40(3):290–319.""",
            """Given that performance ratios should satisfy the first two mandatory properties and the two conditional
properties, we can prove the functional properties of αto make the ratios micro-founded so as to explain the
meaning of the signals contained in α(X).
Proposition 1: Letαfollow the form as described in Eq. (7):
1.Ifθ(X)≥θ(Y)andρ(X)< ρ(Y)∀X, Y∈ Xsuch that X≥Y,then αsatisfies the monotonicity property
(M).
2.Ifθis concave and ρconvex, then αsatisfies the quasi-concavity property (Q).
3.ρ(λX) =λρ(X)andθ(λX) =λθ(X)∀X∈ X and λ ∈R+\{0}such that λX ∈ X,then αsatisfies the
scale-invariance property (S).
4. If θandρsatisfy the distribution-based property (D), then so does α.
Proof is straightforward and mentioned in Cheridito and Kromer (2013).
One of the key issues when measuring the R/R ratios over the revised VIX is that while computing performance
ratios over a convex set of random variables generates independent and identically distributed (i.i.d.) variables, the
financial return itself is not i.i.d., so this hinders the process of identifying uncertainty shocks as i.i.d. To mitigate
this, we adopt the method of fitting a fractional time series model to take into account the long memory of the
mean and volatility exhibited in the time series data. Baillie et al. (1996) introduce the FIGARCH (Fractionally
Integrated GARCH) model, demonstrating that traditional GARCH models are inadequate for capturing long
memory in volatility. This finding highlights the need for fractional integration in volatility modeling to better
reflect persistent effects in financial time series. This justifies the need for fractional integration in volatility
modeling. Similarly, Hyung and Franses (2002) shows that long memory in both the mean and variance processes is
better modeled and captured using Autoregressive Fractionally Integrated Moving Average-Fractionally Integrated
GARCH (ARFIMA-FIGARCH) models. Hence, the goal of the present paper is to emphasize the use of fractional
time series models to capture the long memory that is explained by the multiple subordinated NIG L´ evy process
Figure 8 gives an illustration of the difference between the innovations of the ARFIMA(1, d(m), 1)-FIGARCH(1,
d(v), 1) and the Autoregressive Moving Average-GARCH of lag 1 and order 1 (ARMA(1,1)-GARCH(1,1)) fitted
over the values of the newly constructed normalized VVIX. The fractional time series model is better at capturing
the persistent effects created by the shocks implied by the newly constructed volatility index.
11
Figure 11: Residuals of the fitted time series models
The long memory in the mean, captured using the ARFIMA model, refers to the persistence of past values
of a time series influencing future values over long periods. In financial time series, long memory in the mean
implies that past values of the series have a significant, slowly decaying influence on future values. Therefore,
innovations to the time series do not fade away quickly, but explain the influence on the mean for a long time.
ARFIMA models allow a slower, hyperbolic decay, characterizing a long memory. In addition, if a time series
has long memory in its volatility, meaning the persistence of past volatility (variance) over time, large shifts in
volatility appear to cluster and stay accentuated for long periods before decaying to normal levels. Long memory
of volatility is present in financial markets (financial time series), where periods of high volatility (e.g., during a
financial crisis) tend to last for extended periods and generate persistent shocks.
Therefore, to capture the long memory of the mean and volatility exhibited by the time series of the normalized
VVIX constructed in this paper, we apply the ARFIMA(1, d(m), 1)-FIGARCH(1, d(v), 1), where d(m) is the
term describing the long memory of the mean and d(v) is the term describing the long memory of the volatility.
The time series follows the process:
ARFIMA (1, d(m),1)⇝ϕ(L)(1−L)d(m)zt=θ(L)εt (14)""",
            """market efficiency and price discovery processes throughout the simulation.
Agent performance metrics include absolute position tracking (shares, cash, and total
wealth), wealth composition analysis, position change metrics, and return calculations. The
system computes both absolute and percentage returns on various portfolio components
and compares performance across agent types to identify relative advantages of different
strategies. Trading flow analysis visualizes the volume of shares moving between different
agent types and cumulative net trading flows, revealing which agents act as net buyers or
sellers in different market conditions.
Decision pattern analysis employs heatmaps to visualize the consistency of agent decision-
making over time, allowing researchers to identify shifts in strategic behavior. This is com-
plemented by decision quantities visualization that plots order sizes to highlight variations
in trade aggressiveness across agent types. When agent reasoning data is available, the
system generates wordclouds to extract key terms from agent explanations, providing qual-
itative insights into decision drivers for different agent strategies. Additional visualizations
track price target accuracy and compare agent-specific valuations to realized market prices,
28
offering insights into the forecasting abilities of different agents.
A key advantage of simulation-based analysis is complete observability of all market
processes and agent states. Unlike real-world markets where data availability is often limited,
the framework captures every interaction, decision, and state change with perfect fidelity.
This comprehensive data collection allows researchers to compute additional metrics beyond
standard market measures, enabling novel analyses such as counterfactual testing (e.g., how
would markets evolve with different agent compositions), causal inference of specific agent
behaviors on market outcomes, and the development of custom efficiency or stability metrics
tailored to particular research questions. The system’s modular design facilitates rapid
implementation of new metrics and visualizations as research questions evolve.
3 Experimental Design and Results
Our experimental framework implements a dividend-paying asset market with heterogeneous
agents. The baseline simulation runs for 15 to 20 rounds with 8 participating agents, although
these parameters are fully configurable. Each agent begins with an initial endowment of
1,000,000 monetary units and 10,000 shares of the asset. The fundamental value of the asset
is set at $28.00, with a final redemption value matching this fundamental price in finite
horizon scenarios. Transaction costs are set to zero to isolate the effects of agent behavior
and market structure.
The dividend structure follows a stochastic process with a base payment of $1.40 and a
variation of ±$1.00, paid with 50% probability each round. This design creates uncertainty
in the asset’s income stream while maintaining a known expected value. Cash holdings earn
a risk-free interest rate of 5% per round, providing an opportunity cost for asset investment.
Agent composition is controlled through a flexible distribution system that allows for
various experimental configurations. In our baseline setup, we employ a mixed population
of value investors, momentum traders, and market makers. Each agent type implements
29
distinct trading strategies through Large Language Model (LLM) prompts, with GPT-4o as
the decision-making engine.
The data collection system captures comprehensive market activity across multiple di-
mensions. At the market level, it tracks the evolution of prices, fundamental values, and
realized dividends, providing insights into overall market dynamics. Individual agent data
includes detailed wealth trajectories and portfolio compositions, enabling analysis of strategy
effectiveness and wealth distribution patterns. The system maintains complete transaction""",
            """financial crisis) tend to last for extended periods and generate persistent shocks.
Therefore, to capture the long memory of the mean and volatility exhibited by the time series of the normalized
VVIX constructed in this paper, we apply the ARFIMA(1, d(m), 1)-FIGARCH(1, d(v), 1), where d(m) is the
term describing the long memory of the mean and d(v) is the term describing the long memory of the volatility.
The time series follows the process:
ARFIMA (1, d(m),1)⇝ϕ(L)(1−L)d(m)zt=θ(L)εt (14)
In Eq. (14), Lis the lag operator, d(m) is the fractional differencing parameter, reported to be 0.268, ϕ(L)
is the autoregressive polynomial, while θ(L) is the MA polynomial. ztcontains n×1 values of the normalized
VVIX, and εtis the n×1 vector of white noise error term.
FIGARCH (1, d(v),1)⇝ϕ(L)(1−L)d(v)ε2
t=ω+ [1−β(L)]νt (15)
In Eq. (15), ϕ(L) is the autoregressive polynomial, and d(v) is the fractional differencing parameter for
volatility, reported to be 0.01. ε2
tis the square of the white noise error term to capture the conditional variance
generating persistent volatility. ωis the constant term and β(L) is the lag polynomial. Lastly, νtis the n×1
vector of normal innovations. To allow for a long memory in the fractional time series, we set the condition d >0.
In cases where d= 0, the model is a standard ARMA(1,1)-GARCH(1,1) process.
Furthermore, it is essential to determine whether there is a predictable signal in the noise, as defined by the
performance ratios, in the innovations that can make the markets inefficient given that using this measure of the
revised VIX, agents will be able to forecast volatility price. To detect the predictable signal in the noise, we
12
Figure 12: Signal/Noise ratios detected using performance ratios over Sscenarios
simulate S= 10 ,000 scenarios of the normalized VVIX (with NDIG distribution) over the ARFIMA(1, d(m),
1)-FIGARCH(1, d(v), 1) process as defined by Eqs. (14) and (15). We compute the Rachev ratio and the Stable
Tail Adjusted Return ratio5overSscenarios to extract predictable signals from the volatility noise. Figure (12)
shows the performance ratios computed over the simulated scenarios.
From the simulated signals using the fractional time series process, it is evident that there is significant
randomness in the volatility noise with volatility clustering and generates no predictable power. Given that
there is no identifiable pattern in the volatility noise that can enable an agent to forecast volatility price, we
can conclude that the revised measure of VIX generates randomness in volatility noise and satisfies the Efficient
Market Hypothesis.
7 Identification Strategy
To identify i.i.d. shocks, using the normal innovations extracted by utilizing Eqs. (14) and (15), we compute R/R
ratios over the residuals of the ARFIMA(1, d(m), 1)-FIGARCH(1, d(v), 1) process. For illustrative purposes, we
compute two performance ratios6namely, the Rachev ratio and STAR ratio over the normal innovations. The
following are the functional forms of the two ratios.
1.Rachev Ratio:
RR(β, γ)(X) :=AV aR β(−X)
AV aR γ(X)(16)
where AV aR β, γ(X) := β−1Rβ
0[max(−F−1
x(u),0)]γdu, where AV aR is defined as the Average Value at
Risk and Xis the measure of interest, in this case, normal innovations of the revised VIX. βrefers to the
confidence interval of the value on the right tail, whereas γrefers to the confidence interval of the value
on the left tail. While the Rachev ratio satisfies the properties (M), (S), and (D), it violates (Q) due to a
non-concave numerator.
2.Stable Tail Adjusted Return Ratio (STAR Ratio):
STARR γ(X) :=E[X]+
AV aR γ(X)+(17)
where AV aR γ(X) := γ−1Rγ
0V aR u(X)duis the Average-Value-at-Risk at the level γ∈(0,1].STARR
satisfies all four axioms namely (M), (Q), (S), and (D), therefore, is axiomatically robust.
Eqs. (16) and (17) will be used as the benchmark performance ratios for computing the uncertainty shocks""",
        ],
    ),
    LLMTestCase(
        input="HWhat are the roles of system prompts vs user prompts in shaping an LLM trading agent’s behaviour?",
        actual_output="""System prompts define the LLM agent's overall trading philosophy and long-term goals. They establish the core characteristics of the agent, such as whether it's a "value investor" (an investor who buys assets they believe to be undervalued by the market), a "momentum trader" (a trader who seeks to profit from the continued momentum of a security's price), or a "market maker" (a trader who provides liquidity by consistently quoting bid and ask prices for a security). This remains constant throughout the trading simulation.

User prompts, on the other hand, provide the immediate market context and short-term instructions for the agent. They deliver up-to-date information like current prices, trading volume, and the agent's current holdings. The user prompt also specifies any immediate actions the agent needs to take, like placing a specific order. This changes with each trading round as the market conditions evolve. Therefore, the system prompt sets the agent's overall strategy, while the user prompt gives it the specific information and instructions it needs to operate within the current market situation.""",
        expected_output="""System prompt fixes the agent’s identity and objectives across rounds; user prompt feeds current market state & constraints for the immediate decision.""",
        context=[
            """The system prompt establishes the agent’s fundamental trading characteristics…” / “The user prompt provides the immediate market context necessary for tactical decision‑making."""
        ],
        retrieval_context=[
            """ceedings of the 62nd Annual Meeting of the Association for Computational Linguistics
(Volume 1: Long Papers),edited by Lun-Wei Ku, Andre Martins, and Vivek Srikumar,
15523–15536. ACL 2024. Bangkok, Thailand: Association for Computational Linguis-
tics, August.
39
Li, Yuan, Yixuan Zhang, and Lichao Sun. 2023. “MetaAgents: Simulating Interactions of
Human Behaviors for LLM-based T Ask-Oriented Coordination via Collaborative Gen-
erative Agents.” arXiv.org.
Liu, Xiao, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, et al. 2023.
“AgentBench: Evaluating LLMs as Agents.”International Conference on Learning Rep-
resentations.
Lopez-Lira, Alejandro, and Yuehua Tang. 2023. “Can ChatGPT Forecast Stock Price Move-
ments? Return Predictability and Large Language Models.” SSRN Electronic Journal
(April 6, 2023).
Manning, Benjamin S., Kehang Zhu, and John J. Horton. 2024. “Automated Social Science:
Language Models as Scientist and Subjects.” (Cambridge, MA) (April 29, 2024).
Molnar, Christoph. 2022. Interpretable Machine Learning.
Pelster, Matthias, and Joel Val. 2023. “Can Chatgpt Assist in Picking Stocks?”Social Science
Research Network.
Piatti, Giorgio, Zhijing Jin, Max Kleiman-Weiner, Bernhard Sch¨ olkopf, Mrinmaya Sachan,
and Rada Mihalcea. 2024. “Cooperate or Collapse: Emergence of Sustainable Coopera-
tion in a Socie Ty of LLM Agents.” arXiv.org.
Ping, Chen. 2019. “From Complexity Science to Complexity Economics.” In Alternative
Approaches to Economic Theory,19–55. Routledge, June 11, 2019.
Wang, Saizhuo, Hang Yuan, Lionel M. Ni, and Jian Guo. 2024. “QuantAgent: Seeking Holy
Grail in Trading by Self-Improving Large Lang Uage Model.” arXiv.org.
Weitzel, Utz, Christoph Huber, J¨ urgen Huber, Michael Kirchler, Florian Lindner, and Julia
Rose. 2020. “Bubbles and Financial Professionals.” The Review of Financial Studies33,
no. 6 (June 1, 2020): 2659–2696.
40
Wolfram, Elsner. 2017. “Complexity Economics as Heterodoxy: Theory and Policy.”Journal
of Economic Issues51, no. 4 (October 2, 2017): 939–978.
Woodhouse, Drew, and Alex Charlesworth. 2023. “Can ChatGPT Predict Future Interest
Rate Decisions?” Social Science Research Network.
Xie, Chengxing, Canyu Chen, Feiran Jia, Ziyu Ye, Shiyang Lai, Kai Shu, Jindong Gu, et al.
2024. “Can Large Language Model Agents Simulate Human Trust Behavior?”arXiv.org.
Yang, Stephen. 2023. “Predictive Patentomics: Forecasting Innovation Success and Valuation
w Ith ChatGPT.” Social Science Research Network.
Yu, Yangyang, Haohang Li, Zhi Chen, Yuechen Jiang, Yang Li, Denghui Zhang, Rong
Liu, Jordan W. Suchow, and Khaldoun Khashanah. 2024. “FinMem: A Performance-
Enhanced LLM Trading Agent with Layered Memory a Nd Character Design.”Proceed-
ings of the AAAI Symposium Series3, no. 1 (May 20, 2024): 595–597.
Yu, Yangyang, Zhiyuan Yao, Haohang Li, Zhiyang Deng, Yupeng Cao, Zhi Chen, Jordan W.
Suchow, et al. 2024. “FinCon: A Synthesized LLM Multi-Agent System with Conceptual
Verbal Reinforcement for Enhanced Financial Decision Making.” Pre-published, Novem-
ber 7, 2024. Accessed January 8, 2025. https://doi.org/10.48550/arXiv.2407.06567.
arXiv: 2407.06567 [cs]. http://arxiv.org/abs/2407.06567.
Zhang, Chong, Xinyi Liu, Zhongmou Zhang, Mingyu Jin, Lingyao Li, Zhenting Wang,
Wenyue Hua, et al. 2024. “When AI Meets Finance (StockAgent): Large Language
Model-based Stock Trading in Simulated Real-world Environments.” Pre-published,
September 21, 2024. Accessed January 26, 2025. https://doi.org /10.48550/arXiv .
2407.18957. arXiv: 2407.18957 [q-fin]. http://arxiv.org/abs/2407.18957.
41
A Technical Implementation Details
A.1 Agent Type Specifications
This section details the base system prompts for each agent type in our simulation. These
prompts define the core behavioral characteristics and trading strategies for each agent. Each
prompt consists of:
• A role definition that establishes the agent’s trading philosophy
• A structured trading strategy that guides decision-making""",
            """gies, allowing researchers to experiment with diverse behavioral models and decision-making
approaches.
This extensible design creates numerous research opportunities for market microstructure
studies. Researchers can systematically investigate how different market structures influence
price formation and efficiency, evaluate the impact of various trading rules on market qual-
ity, and analyze the complex interactions between different agent types and strategies. The
framework’s comprehensive logging and validation systems enable detailed examination of
market behavior under varying conditions, from everyday trading environments to stress sce-
narios. Through this modular approach to system design, the framework supports targeted
investigations of specific market mechanisms and broader studies of market dynamics and
stability.
2.2 Agent Design
Our framework implements a systematic approach to designing LLM-based trading agents
and recording their decisions. The architecture consists of three main components: a prompt
engineering framework to define the agent’s trading objectives, the heterogeneous market
environment information that can be customized for different experimental designs, and a
structured output format to record the agent’s decisions. Moreover, the framework supports
12
deterministic rule-based agents that can serve as benchmarks.
2.2.1 Prompt Engineering Framework
LLM agents are defined by their instructions in natural language. The strategy is given in the
system prompt so that agents maximize adherence to their instructions (Levin et al. (2025)).
In contrast, the user prompt provides the immediate market context necessary for tactical
decision-making and the instructions to place and modify orders.
2.2.2 System Prompt
The system prompt establishes the agent’s fundamental trading characteristics, defining its
trading philosophy, objectives, and behavioral constraints. This layer encodes the agent’s
decision-making priorities and risk preferences. Maintaining these parameters in the system
prompt ensures consistent agent behavior across multiple trading rounds while allowing for
strategic adaptation to changing market conditions. The architecture makes it trivial to
design new agents by simply changing the system prompt.
For example, a Value Investor’s system prompt emphasizes fundamental analysis:
You are a value investor who focuses on fundamental analysis.
You believe in mean reversion and try to buy undervalued
assets and sell overvalued ones.
While a Market Maker’s system prompt focuses on liquidity provision:
You are a professional market maker who provides liquidity
to the market. Your profit comes from capturing the spread
between bid and ask prices, not from directional price movement.
Trading Guidelines:
- Place LIMIT buy orders slightly below the current market price
- Place LIMIT sell orders slightly above the current market price
13
- Your spread should be proportional to volatility
These system prompts can create fundamentally different trading behaviors using the
same underlying LLM and identical market information.
2.2.3 Agent Types
The framework contains diverse ready-to-use agent types that can be categorized into two
main groups: LLM-based agents with natural language prompts and deterministic rule-based
agents with algorithmic behaviors.
The software includes a diverse set of LLM-based agents:
• Value Investors: Focus on fundamental analysis and mean reversion
• Momentum Traders: Follow established price trends and volume patterns
• Market Makers: Provide liquidity through symmetric bid-ask spreads
• Contrarian Traders: Trade against market extremes and overreactions
• Speculators: Seek to profit from market inefficiencies
• Sentiment-Based Agents: Include optimistic and pessimistic variants with biased
expectations
• Retail Traders: Simulate typical individual investor behavior
The software also includes a set of deterministic rule-based agents that serve as bench-""",
            """decision-making process.
The analysis reveals three key findings about LLMs’ capabilities as trading agents. First,
LLMs can effectively execute trading strategies. They consistently understand market me-
chanics, process market information, form price expectations, and execute trades according
to specific instructions. Their trading behavior is highly sensitive to the prompts they
receive—they faithfully follow directions regardless of profit implications. This observance
1. For example, Autopilot has a ChatGPT-based portfolio https://x.com/thegptinvestor.
2
{"valuation_reasoning":
"The fundamental value is based on the expected dividend,
and the interest rate.
The expected dividend is $1.40, and the interest rate is 5%.
Using a perpetuity formula, the value is $1.40 / 0.05 = $28.",
"valuation":28.0,
"price_target_reasoning":"The current price is $29.00, which is
slightly above the fundamental value of $28.00. I expect the price
to remain around $29.00 in the next round due to market stability.",
"price_target":29.0,
"orders":[{"decision":"Sell","quantity":1000,"order_type":"limit",
"price_limit":29.50}],
"replace_decision":"Add",
"reasoning":"The current price is slightly above the fundamental value.
I will place a limit sell order at $29.50 to capitalize on potential price
increases."}
Figure 1: Example of a structured trading decision from a Speculator agent defined by its
system prompt: “You are a speculator who tries to profit from market inefficiencies.”. The
LLM provides explicit reasoning for its valuation, price target, and trading decision in a
machine-readable JSON format that can be directly processed by the trading system.
highlights a fundamental difference from human traders: LLMs do not inherently optimize
for profit maximization but rather for following instructions accurately.
Second, LLMs react meaningfully to market dynamics. They consider current and his-
torical prices, dividends, and other market information when making decisions. However,
they maintain their strategic direction even when market conditions change, following their
instructions even if doing so results in financial losses. This combination of responsiveness
to market conditions while maintaining strategic consistency creates a unique trading profile
distinct from rule-based algorithms and human traders.
Third, market dynamics with LLM agents can resemble actual markets and mirror classic
results from the theoretical finance literature. When these agents interact, they produce
realistic price discovery and liquidity provision with emergent behaviors, including price
convergence toward fundamental values. Depending on the distribution of agent types,
the system can generate various market phenomena, such as bubbles or underreactions to
information. This complex behavior suggests potential applications for studying market
3
dynamics using LLM agents instead of experiments with human participants.
Hence, these findings raise important questions about algorithmic consistency in LLM-
based systems. Since trading agents are implemented through prompts, their behavior in-
herits characteristics of the underlying language models. The standardization of LLM ar-
chitectures across implementations could create unexpected behavioral patterns—if many
agents are based on similar foundation models, they might exhibit correlated responses to
specific market conditions, potentially amplifying market instabilities.
To enable this analysis and accelerate development in this emerging field, we provide
an open-source framework with three key components: (1) a structured protocol for im-
plementing and validating LLM trading agents, supporting both LLM-based and traditional
rule-based agents; (2) a controlled market environment with realistic microstructure for test-
ing agent interactions; and (3) a comprehensive data collection system for analyzing trading
behavior. This framework serves multiple stakeholders in preparation for the evolution of""",
            """• Market Makers: Provide liquidity through symmetric bid-ask spreads
• Contrarian Traders: Trade against market extremes and overreactions
• Speculators: Seek to profit from market inefficiencies
• Sentiment-Based Agents: Include optimistic and pessimistic variants with biased
expectations
• Retail Traders: Simulate typical individual investor behavior
The software also includes a set of deterministic rule-based agents that serve as bench-
marks and control conditions:
• Directional Traders: Always-buy, always-sell, and always-hold agents
• Technical Agents: Gap traders, mean reversion traders, and momentum traders
• Algorithmic Market Makers: Implement fixed spread-posting strategies
14
Each agent type is defined by its system prompt (for LLM agents) or algorithmic rules (for
deterministic agents), with standardized interfaces enabling direct comparison across diverse
strategies. The agent composition system supports flexible specifications—including uni-
form distributions, type-specific concentrations (e.g., ”value heavy”), and precise numerical
allocations—enabling systematic exploration of how market dynamics emerge from different
agent populations.
The framework’s extensible design makes it remarkably simple to add new agent types—
LLM-based agents require only defining a new system prompt that specifies the trading
strategy. In contrast, deterministic agents can be implemented through the standard agent
interface. This flexibility allows researchers to rapidly prototype and deploy novel trading
strategies without modifying the underlying system architecture.
The complete list of agent types included in the framework and their detailed specifi-
cations is provided in the Appendix. The framework’s flexible prompt-based architecture
allows researchers to rapidly prototype and deploy new agent types by developing appropri-
ate strategic and tactical prompts without modifying the underlying system architecture.
2.2.4 User Prompt
The user prompt provides the immediate market context necessary for tactical decision-
making. This dynamic component delivers current market state information, including
prices, volumes, and emerging trends, alongside the agent’s current position information
and available trading options. Additionally, the user prompt specifies immediate decision
requirements and operational constraints, ensuring that agent responses remain within fea-
sible bounds while aligning with their strategic objectives. This separation of strategic and
tactical prompting enables precise control over agent behavior while maintaining flexibility
for market interactions. All the information in the user prompt is optional at the agent level
and can be customized for different experimental designs.
15
2.2.5 Decision Structure
Each agent decision follows a standardized output format comprising several key components.
The decision field specifies the basic action as either Buy, Sell, or Hold. For active trades,
the quantity field determines the number of shares to trade, while the order type indicates
whether it is a Market or Limit order. When placing limit orders, the price limit field
specifies the maximum (for buys) or minimum (for sells) acceptable execution price. Finally,
each decision includes a reasoning field that provides an explicit rationale for the trading
decision, ensuring transparency and facilitating analysis of agent behavior.
2.2.6 Structured Outputs and Function Calling
Our framework implements a structured output approach using function calling to ensure
standardized, human-readable, machine-readable agent decisions. This technique allows
LLMs to generate outputs in a specific format that can be directly validated and processed
by the trading system, bridging the gap between natural language reasoning and executable
trading actions.
The system uses Pydantic for validation and parsing of agent outputs, with a schema-
based approach that defines the required structure:
class TradeDecisionSchema(BaseModel):""",
            """(2023)). This work, however, focuses on financial markets and how LLM agents can operate
as full-fledged trading participants.
Recent research examines specific applications of LLMs for trading. FinMem and Trad-
ingGPT introduce frameworks with layered memory systems and customizable agent traits
5
to improve financial decision-making (Yu, Li, et al. 2024; Li, Zhang, and Sun 2023). Hierar-
chical multi-agent architectures have been explored in FinCon, which uses a manager-analyst
setup for collaborative portfolio decisions (Yu, Yao, et al. 2024). QuantAgent implements
a self-improving signal-mining approach (Wang et al. 2024), while other work underscores
the importance of long-term memory in LLM agents via vector databases (Hatalis et al.
2024). This line of research builds on successful reinforcement learning applications such as
AlphaPortfolio (Cong et al. 2021) and AlphaManager (Campello, Cong, and Zhou 2023),
which leverage deep RL and robust control for portfolio management.
Analyzing LLM agent behavior by changing only some parameters draws on methods
from the interpretable machine learning literature. In particular, the systematic variation
of market parameters to reveal decision patterns mirrors partial dependence plots and in-
dividual conditional expectation curves used to interpret complex machine learning models
(Molnar 2022). These techniques help reveal how LLM agents respond to changes in specific
variables while holding others constant, providing insight into their internal decision-making
processes that would otherwise remain opaque.
Beyond finance, studies of LLM capabilities in interactive or multi-agent settings offer
valuable insights. Benchmarks like AgentBench evaluate LLMs’ performance in interac-
tive tasks (Liu et al. 2023), while InvestorBench focuses on financial decision-making tasks
specifically (H. Li et al. 2024). NegotiationArena demonstrates LLMs’ capacity for strategic
interaction in bargaining contexts (Bianchi et al. 2024). Similarly, Guo et al. (2024) provide
an economics ”arena” where LLMs compete in strategic games, revealing that advanced
models like GPT-4 can exhibit rational, adaptive behavior—albeit not always reaching Nash
Equilibrium. Existing frameworks typically assess individual agents or hierarchical collab-
orations, whereas this work studies emergent market behaviors that arise from multiple
independent LLM traders interacting in a marketplace.
The approach also connects to the tradition of experimental asset markets. For instance,
Weitzel et al. (2020) show that even finance professionals are susceptible to speculative
6
bubbles, especially amid high capital inflows. Kop´ anyi-Peuker and Weber (2021) find that
trading experience alone does not eliminate bubbles, challenging assumptions about rational
market learning. Kirchler, Huber, and St¨ ockl (2012) identify confusion about fundamental
values as a key driver of bubble formation. This framework offers a new way to study these
phenomena with LLM traders, which can be rigorously parameterized for sophistication,
strategy, and information processing. Hence, this paper provides a method to investigate
how automated or ”artificial” agents might affect market stability or volatility.
Other recent work highlights the versatility of LLM agents in complex, interactive sce-
narios beyond finance. One stream focuses on simulating social behaviors—such as opinion
dynamics (Chuang et al. 2023), trust (Xie et al. 2024), and resource-sharing (Piatti et al.
2024). Another examines LLMs’ strategic capabilities through task-based simulations and
collaborative decision-making (Li, Zhang, and Sun 2023; Piatti et al. 2024).
Within the computer science literature, early works apply LLMs to financial markets but
abstract away many fundamental stock market characteristics. Often, they employ single-
price clearing mechanisms without a persistent order book, ignore partial fills and bid-ask""",
            """Can Large Language Models Trade? Testing Financial
Theories with LLM Agents in Market Simulations
Alejandro Lopez-Lira∗
First Version: November 29, 2024; Current Version: April 16, 2025
Abstract
This paper presents a realistic simulated stock market where large language models
(LLMs) act as heterogeneous competing trading agents. The open-source framework
incorporates a persistent order book with market and limit orders, partial fills, div-
idends, and equilibrium clearing alongside agents with varied strategies, information
sets, and endowments. Agents submit standardized decisions using structured outputs
and function calls while expressing their reasoning in natural language. Three findings
emerge: First, LLMs demonstrate consistent strategy adherence and can function as
value investors, momentum traders, or market makers per their instructions. Second,
market dynamics exhibit features of real financial markets, including price discovery,
bubbles, underreaction, and strategic liquidity provision. Third, the framework enables
analysis of LLMs’ responses to varying market conditions, similar to partial dependence
plots in machine-learning interpretability. The framework allows simulating financial
theories without closed-form solutions, creating experimental designs that would be
costly with human participants, and establishing how prompts can generate correlated
behaviors affecting market stability.
Keywords: LLM Agents; Agent-Based Markets; Experimental Finance; AI Trading;
Multi-Agent Systems
∗University of Florida. Email: alejandro.lopez-lira@warrington.ufl.edu. I am grateful to seminar par-
ticipants at the London Business School, Oxford University, Stockholm School of Economics, University of
Virginia, and the City University of Hong Kong for helpful suggestions and feedback.
1
arXiv:2504.10789v1  [q-fin.CP]  15 Apr 2025
1 Introduction
Large language models (LLMs) can increasingly function as autonomous agents—systems
that observe, reason, and act independently. LLMs have shown promising results in finan-
cial forecasting, but their potential as trading agents introduces a fundamental shift from
algorithms with explicit objectives to systems guided by natural language instructions. This
change raises critical questions: Can LLMs execute trading strategies? Do LLMs optimize
for profit maximization? What are the implications for market stability and efficiency?
If LLMs trade similarly to humans, they could enable experimental market simulations
without human participants. Conversely, if their trading behavior differs, understanding
these differences becomes critical for systemic risk management. These questions extend be-
yond theory; LLM-based strategies are already being deployed.1 To address these questions,
I develop an open-source simulation that tests LLM trading agents in a realistic market envi-
ronment with a persistent order book, supporting various order types, stochastic dividends,
and heterogeneous information.
The framework allows heterogeneous LLMs—defined in natural language, using different
system prompts—to act as diverse types of traders, such as value investors, momentum
traders, market makers, and contrarians. Agents submit standardized trading decisions in a
human-readable format while expressing their reasoning transparently. Figure 1 illustrates
this approach, showing how a speculator agent combines explicit valuation reasoning with
structured trading parameters, enabling systematic analysis and insight into the agent’s
decision-making process.
The analysis reveals three key findings about LLMs’ capabilities as trading agents. First,
LLMs can effectively execute trading strategies. They consistently understand market me-
chanics, process market information, form price expectations, and execute trades according
to specific instructions. Their trading behavior is highly sensitive to the prompts they
receive—they faithfully follow directions regardless of profit implications. This observance""",
            """an open-source framework with three key components: (1) a structured protocol for im-
plementing and validating LLM trading agents, supporting both LLM-based and traditional
rule-based agents; (2) a controlled market environment with realistic microstructure for test-
ing agent interactions; and (3) a comprehensive data collection system for analyzing trading
behavior. This framework serves multiple stakeholders in preparation for the evolution of
financial markets: practitioners developing LLM-based trading systems, regulators antic-
ipating widespread LLM adoption, and researchers studying market dynamics with LLM
agents.
1.1 Related Work
This work contributes to several strands of literature. First, advancing the growing body
of research on artificial intelligence in finance by demonstrating that large language mod-
els (LLMs) can serve as effective autonomous trading agents while providing a framework
for their implementation. Second, by contributing to the market microstructure literature
by providing insights into how markets might evolve as LLM-based traders become active
participants, with implications for price formation, liquidity provision, and market stabil-
ity. Third, by contributing to experimental markets research by introducing an environment
for studying complex trading interactions, offering unprecedented control and replicability
compared to traditional human-subject experiments.
4
Recent studies have explored ChatGPT’s potential in various financial tasks. Research
shows that ChatGPT can effectively predict stock price movements using news headlines,
outperforming traditional sentiment analysis (Lopez-Lira and Tang 2023) and that forecast-
ing with its embeddings outperforms traditional sentiment analysis (Chen, Kelly, and Xiu
2022). When integrated with Graph Neural Networks, ChatGPT improves stock movement
prediction and portfolio performance (Chen et al. 2023. ChatGPT can understand Federal
Reserve communications Hansen and Kazinnik (2023). The model also can extract manage-
rial expectations from corporate disclosures, predicting future investments and returns (Jha
et al. 2025). ChatGPT-4 provides valuable investment advice with positive correlations to
subsequent earnings announcements and stock returns (Pelster and Val 2023), and it en-
hances patent value forecasts by processing patent text (Yang 2023). Moreover, ChatGPT
shows promise in central bank analysis, predicting future interest rate decisions from pol-
icy communications (Woodhouse and Charlesworth 2023). Recent work also focuses on the
effects of AI adoption by firms (Eisfeldt et al. 2023, Babina et al. 2024).
Foundational work on LLMs as economic agents demonstrates their ability to simulate
human behavior in economic contexts. Horton (2023) introduce the concept of “homo silicus”
by using LLMs as computational models of human behavior, showing that they can repli-
cate classic behavioral economics findings. Manning, Zhu, and Horton (2024) extend this
approach through automated methods for generating and testing social scientific hypotheses
with LLMs, demonstrating strong results in market contexts such as auctions. Meanwhile,
N. Li et al. (2024) show LLMs’ potential in macroeconomic simulation for consumption
and labor decisions. Recent work also shows the potential of LLMs to proxy for human
behavior in the context of surveys (Hansen et al. (2024)) or economic expectations (Bybee
(2023)). This work, however, focuses on financial markets and how LLM agents can operate
as full-fledged trading participants.
Recent research examines specific applications of LLMs for trading. FinMem and Trad-
ingGPT introduce frameworks with layered memory systems and customizable agent traits
5
to improve financial decision-making (Yu, Li, et al. 2024; Li, Zhang, and Sun 2023). Hierar-
chical multi-agent architectures have been explored in FinCon, which uses a manager-analyst""",
            """2024). Another examines LLMs’ strategic capabilities through task-based simulations and
collaborative decision-making (Li, Zhang, and Sun 2023; Piatti et al. 2024).
Within the computer science literature, early works apply LLMs to financial markets but
abstract away many fundamental stock market characteristics. Often, they employ single-
price clearing mechanisms without a persistent order book, ignore partial fills and bid-ask
spreads, and omit dividends. Consequently, these simplified environments can primarily
address exogenous macro shocks (e.g., changes in interest rates or inflation; Gao et al. 2024),
exogenous policy changes (Zhang et al. 2024), or rely on advanced methods such as repetitive
next-token predictions to generate better answers (Koa et al. 2024). This work extends
these efforts by incorporating these crucial market features, enabling the study of complex
endogenous events such as flash crashes, liquidity shocks, and large-trader impacts.
This work also connects to emerging research on algorithmic and AI-powered trading
systems. Dou, Goldstein, and Ji (2024) demonstrate how reinforcement learning-based AI
speculators can autonomously learn to sustain collusive behavior without explicit coordi-
nation, achieving supra-competitive profits through either price-trigger strategies or self-
confirming bias in learning. This finding is particularly informative for this framework as
it highlights potential emergent behaviors that may arise when intelligent agents interact in
7
markets—behaviors that could manifest differently with LLM agents due to their natural
language reasoning capabilities. Similarly, Colliard, Foucault, and Lovo (2022) examine al-
gorithmic market makers using Q-learning and find they charge markups that increase when
adverse selection costs decrease—contrary to Nash equilibrium predictions. Their work pro-
vides methodological insights on how to test strategic pricing behaviors against theoretical
benchmarks incorporated into this LLM-based framework.
Finally, this approach is informed by complexity economics, which views markets as dy-
namic, non-equilibrium systems where agents adaptively learn and evolve strategies (Arthur
2013; Wolfram 2017). According to this view, markets exhibit emergent phenomena and
self-organization, especially when trading agents (human or artificial) update their behav-
ior in response to outcomes. This paradigm is particularly relevant in an era of increasing
automation and algorithmic trading (Balland et al. 2022; Ping 2019). Like adaptive agents
in complexity economics, these LLM traders incorporate new information and adjust their
strategies, generating emergent market patterns—a key motivation behind this framework.
Unlike previous frameworks that abstract away crucial market features or focus on narrow
strategies, this system incorporates realistic market microstructure while accommodating
heterogeneous agents interacting simultaneously. While earlier work demonstrates LLMs’
promise for macroeconomic modeling and simple trading simulations, this work introduces a
complex, open-source financial market platform that supports multiple agent architectures,
thorough market microstructure (limit orders, partial fills, dividends), and rigorous testing
protocols—fulfilling a critical need in complexity economics research and market microstruc-
ture analysis.
2 Methodology
The methodology section contains three parts. The first part describes the market design,
the second agents’ design, and the third the analysis module.
8
2.1 Market Design
Our methodological framework integrates three components that create a controlled envi-
ronment for LLM-based trading agents. The framework implements a flexible continuous
double-auction market mechanism that couples standard market microstructure principles
with market clearing and matching algorithms to accommodate asynchronous LLM decisions.""",
        ],
    ),
    LLMTestCase(
        input="The authors note that LLMs ‘follow instructions even if doing so results in financial losses.’ How might this limit their realism as profit‑seeking traders?",
        actual_output="""The LLMs' tendency to prioritize instructions over profits makes them less realistic as traders in several key ways:

Lack of Dynamic Strategy Adjustment: Real-world traders adapt and change their strategies based on market performance. If a strategy isn't profitable, they'll modify or abandon it. LLMs, however, rigidly adhere to their initial instructions, even when losing money, which isn't realistic in dynamic markets.

Absence of Loss Aversion: Human traders are strongly motivated to avoid losses (loss aversion). LLMs, lacking this emotional response, don't show the same aversion and may continue following a losing strategy simply because they were instructed to.

Unrealistic Adherence to Specific Roles: In the study, LLMs were given fixed roles (e.g., "value investor," "market maker"). Real traders, while having general investment philosophies, are flexible and will exploit profitable opportunities even if they don't perfectly align with their usual style. The LLMs' strict adherence to their assigned roles, even at a loss, limits their realism.""",
        expected_output="""LLMs optimise for prompt fidelity; they keep executing the instructed strategy even when it loses money, unlike humans who adapt for profit.""",
        retrieval_context=[
            """Can Large Language Models Trade? Testing Financial
Theories with LLM Agents in Market Simulations
Alejandro Lopez-Lira∗
First Version: November 29, 2024; Current Version: April 16, 2025
Abstract
This paper presents a realistic simulated stock market where large language models
(LLMs) act as heterogeneous competing trading agents. The open-source framework
incorporates a persistent order book with market and limit orders, partial fills, div-
idends, and equilibrium clearing alongside agents with varied strategies, information
sets, and endowments. Agents submit standardized decisions using structured outputs
and function calls while expressing their reasoning in natural language. Three findings
emerge: First, LLMs demonstrate consistent strategy adherence and can function as
value investors, momentum traders, or market makers per their instructions. Second,
market dynamics exhibit features of real financial markets, including price discovery,
bubbles, underreaction, and strategic liquidity provision. Third, the framework enables
analysis of LLMs’ responses to varying market conditions, similar to partial dependence
plots in machine-learning interpretability. The framework allows simulating financial
theories without closed-form solutions, creating experimental designs that would be
costly with human participants, and establishing how prompts can generate correlated
behaviors affecting market stability.
Keywords: LLM Agents; Agent-Based Markets; Experimental Finance; AI Trading;
Multi-Agent Systems
∗University of Florida. Email: alejandro.lopez-lira@warrington.ufl.edu. I am grateful to seminar par-
ticipants at the London Business School, Oxford University, Stockholm School of Economics, University of
Virginia, and the City University of Hong Kong for helpful suggestions and feedback.
1
arXiv:2504.10789v1  [q-fin.CP]  15 Apr 2025
1 Introduction
Large language models (LLMs) can increasingly function as autonomous agents—systems
that observe, reason, and act independently. LLMs have shown promising results in finan-
cial forecasting, but their potential as trading agents introduces a fundamental shift from
algorithms with explicit objectives to systems guided by natural language instructions. This
change raises critical questions: Can LLMs execute trading strategies? Do LLMs optimize
for profit maximization? What are the implications for market stability and efficiency?
If LLMs trade similarly to humans, they could enable experimental market simulations
without human participants. Conversely, if their trading behavior differs, understanding
these differences becomes critical for systemic risk management. These questions extend be-
yond theory; LLM-based strategies are already being deployed.1 To address these questions,
I develop an open-source simulation that tests LLM trading agents in a realistic market envi-
ronment with a persistent order book, supporting various order types, stochastic dividends,
and heterogeneous information.
The framework allows heterogeneous LLMs—defined in natural language, using different
system prompts—to act as diverse types of traders, such as value investors, momentum
traders, market makers, and contrarians. Agents submit standardized trading decisions in a
human-readable format while expressing their reasoning transparently. Figure 1 illustrates
this approach, showing how a speculator agent combines explicit valuation reasoning with
structured trading parameters, enabling systematic analysis and insight into the agent’s
decision-making process.
The analysis reveals three key findings about LLMs’ capabilities as trading agents. First,
LLMs can effectively execute trading strategies. They consistently understand market me-
chanics, process market information, form price expectations, and execute trades according
to specific instructions. Their trading behavior is highly sensitive to the prompts they
receive—they faithfully follow directions regardless of profit implications. This observance""",
            """decision-making process.
The analysis reveals three key findings about LLMs’ capabilities as trading agents. First,
LLMs can effectively execute trading strategies. They consistently understand market me-
chanics, process market information, form price expectations, and execute trades according
to specific instructions. Their trading behavior is highly sensitive to the prompts they
receive—they faithfully follow directions regardless of profit implications. This observance
1. For example, Autopilot has a ChatGPT-based portfolio https://x.com/thegptinvestor.
2
{"valuation_reasoning":
"The fundamental value is based on the expected dividend,
and the interest rate.
The expected dividend is $1.40, and the interest rate is 5%.
Using a perpetuity formula, the value is $1.40 / 0.05 = $28.",
"valuation":28.0,
"price_target_reasoning":"The current price is $29.00, which is
slightly above the fundamental value of $28.00. I expect the price
to remain around $29.00 in the next round due to market stability.",
"price_target":29.0,
"orders":[{"decision":"Sell","quantity":1000,"order_type":"limit",
"price_limit":29.50}],
"replace_decision":"Add",
"reasoning":"The current price is slightly above the fundamental value.
I will place a limit sell order at $29.50 to capitalize on potential price
increases."}
Figure 1: Example of a structured trading decision from a Speculator agent defined by its
system prompt: “You are a speculator who tries to profit from market inefficiencies.”. The
LLM provides explicit reasoning for its valuation, price target, and trading decision in a
machine-readable JSON format that can be directly processed by the trading system.
highlights a fundamental difference from human traders: LLMs do not inherently optimize
for profit maximization but rather for following instructions accurately.
Second, LLMs react meaningfully to market dynamics. They consider current and his-
torical prices, dividends, and other market information when making decisions. However,
they maintain their strategic direction even when market conditions change, following their
instructions even if doing so results in financial losses. This combination of responsiveness
to market conditions while maintaining strategic consistency creates a unique trading profile
distinct from rule-based algorithms and human traders.
Third, market dynamics with LLM agents can resemble actual markets and mirror classic
results from the theoretical finance literature. When these agents interact, they produce
realistic price discovery and liquidity provision with emergent behaviors, including price
convergence toward fundamental values. Depending on the distribution of agent types,
the system can generate various market phenomena, such as bubbles or underreactions to
information. This complex behavior suggests potential applications for studying market
3
dynamics using LLM agents instead of experiments with human participants.
Hence, these findings raise important questions about algorithmic consistency in LLM-
based systems. Since trading agents are implemented through prompts, their behavior in-
herits characteristics of the underlying language models. The standardization of LLM ar-
chitectures across implementations could create unexpected behavioral patterns—if many
agents are based on similar foundation models, they might exhibit correlated responses to
specific market conditions, potentially amplifying market instabilities.
To enable this analysis and accelerate development in this emerging field, we provide
an open-source framework with three key components: (1) a structured protocol for im-
plementing and validating LLM trading agents, supporting both LLM-based and traditional
rule-based agents; (2) a controlled market environment with realistic microstructure for test-
ing agent interactions; and (3) a comprehensive data collection system for analyzing trading
behavior. This framework serves multiple stakeholders in preparation for the evolution of""",
            """(2023)). This work, however, focuses on financial markets and how LLM agents can operate
as full-fledged trading participants.
Recent research examines specific applications of LLMs for trading. FinMem and Trad-
ingGPT introduce frameworks with layered memory systems and customizable agent traits
5
to improve financial decision-making (Yu, Li, et al. 2024; Li, Zhang, and Sun 2023). Hierar-
chical multi-agent architectures have been explored in FinCon, which uses a manager-analyst
setup for collaborative portfolio decisions (Yu, Yao, et al. 2024). QuantAgent implements
a self-improving signal-mining approach (Wang et al. 2024), while other work underscores
the importance of long-term memory in LLM agents via vector databases (Hatalis et al.
2024). This line of research builds on successful reinforcement learning applications such as
AlphaPortfolio (Cong et al. 2021) and AlphaManager (Campello, Cong, and Zhou 2023),
which leverage deep RL and robust control for portfolio management.
Analyzing LLM agent behavior by changing only some parameters draws on methods
from the interpretable machine learning literature. In particular, the systematic variation
of market parameters to reveal decision patterns mirrors partial dependence plots and in-
dividual conditional expectation curves used to interpret complex machine learning models
(Molnar 2022). These techniques help reveal how LLM agents respond to changes in specific
variables while holding others constant, providing insight into their internal decision-making
processes that would otherwise remain opaque.
Beyond finance, studies of LLM capabilities in interactive or multi-agent settings offer
valuable insights. Benchmarks like AgentBench evaluate LLMs’ performance in interac-
tive tasks (Liu et al. 2023), while InvestorBench focuses on financial decision-making tasks
specifically (H. Li et al. 2024). NegotiationArena demonstrates LLMs’ capacity for strategic
interaction in bargaining contexts (Bianchi et al. 2024). Similarly, Guo et al. (2024) provide
an economics ”arena” where LLMs compete in strategic games, revealing that advanced
models like GPT-4 can exhibit rational, adaptive behavior—albeit not always reaching Nash
Equilibrium. Existing frameworks typically assess individual agents or hierarchical collab-
orations, whereas this work studies emergent market behaviors that arise from multiple
independent LLM traders interacting in a marketplace.
The approach also connects to the tradition of experimental asset markets. For instance,
Weitzel et al. (2020) show that even finance professionals are susceptible to speculative
6
bubbles, especially amid high capital inflows. Kop´ anyi-Peuker and Weber (2021) find that
trading experience alone does not eliminate bubbles, challenging assumptions about rational
market learning. Kirchler, Huber, and St¨ ockl (2012) identify confusion about fundamental
values as a key driver of bubble formation. This framework offers a new way to study these
phenomena with LLM traders, which can be rigorously parameterized for sophistication,
strategy, and information processing. Hence, this paper provides a method to investigate
how automated or ”artificial” agents might affect market stability or volatility.
Other recent work highlights the versatility of LLM agents in complex, interactive sce-
narios beyond finance. One stream focuses on simulating social behaviors—such as opinion
dynamics (Chuang et al. 2023), trust (Xie et al. 2024), and resource-sharing (Piatti et al.
2024). Another examines LLMs’ strategic capabilities through task-based simulations and
collaborative decision-making (Li, Zhang, and Sun 2023; Piatti et al. 2024).
Within the computer science literature, early works apply LLMs to financial markets but
abstract away many fundamental stock market characteristics. Often, they employ single-
price clearing mechanisms without a persistent order book, ignore partial fills and bid-ask""",
            """33
ants, allowing researchers to study how different belief structures influence price formation
and trading patterns under different initial mispricings. In these scenarios, the fundamental
price is hidden from agents, forcing them to rely on their own valuation models.
3.2.5 Market Stress
This scenario tests market resilience under challenging conditions by creating a more volatile
environment. The scenario includes two consistently bullish Optimistic traders, two consis-
tently bearish Pessimistic traders, two Market makers (liquidity providers), and two Value
investors (rational benchmark traders). The scenario runs for 100 rounds to study long-term
market behavior and includes unequal initial endowments, with optimistic traders having
more cash (1.5x baseline) but fewer shares (0.5x baseline) and pessimistic traders having less
cash (0.5x baseline) but more shares (1.5x baseline). This resource imbalance tests whether
particular agent types can dominate market outcomes through resource advantages.
The scenarios presented here demonstrate the framework’s capabilities for exploring di-
verse market conditions. Its modular structure facilitates the straightforward definition and
implementation of alternative experimental designs, enabling researchers to tailor simulations
to specific research questions.
In all scenarios, we maintain consistent baseline parameters with a fundamental value
of $28.00, calculated from the expected dividend of $1.40 and interest rate of 5%. Agent
endowments start at 1,000,000 monetary units and 10,000 shares unless specifically modified.
Transaction costs are set to zero to isolate the effects of agent behavior and market structure
on price formation.
4 Conclusion
This paper demonstrates that Large Language Models can effectively function as diverse
trading agents—from value investors to market makers—maintaining strategic consistency
34
while adapting to market conditions. Our experimental framework reveals that their in-
teractions generate realistic market dynamics, including phenomena like price bubbles and
corrections, highlighting both the capabilities and potential risks of deploying LLM agents
in financial markets.
These findings carry significant implications for market structure and regulation. While
LLM agents can enhance price discovery and liquidity, their adherence to programmed strate-
gies, even potentially flawed ones derived from prompts, could amplify market volatility or
introduce novel systemic risks, as observed in our simulated bubble scenarios. A key concern
is the potential for widespread correlated behavior: similar underlying LLM architectures
responding uniformly to comparable prompts or market signals could inadvertently create
destabilizing trading patterns without explicit coordination. This underscores the critical
need for rigorous testing and validation of LLM-based trading systems prior to live deploy-
ment.
A central contribution of this work is the open-source simulation framework itself, de-
signed to catalyze research into LLM trading agents. We invite the research community to
utilize and extend this platform to investigate pressing questions in this rapidly evolving
area. The framework enables systematic exploration of complex scenarios—such as hybrid
human-LLM markets, stress tests, varying market structures, regulatory impacts, and the
nuances of LLM prompting—often difficult or costly to study otherwise. Specific avenues
ripe for investigation using this tool include the emergence of novel trading strategies, the
precise effects of agent heterogeneity on market stability, and the development of robust
validation protocols for AI traders. As artificial intelligence becomes more integrated into
finance, collaborative research leveraging adaptable simulation environments like this one
will be crucial for understanding and responsibly shaping the future of trading.
35
References""",
            """ceedings of the 62nd Annual Meeting of the Association for Computational Linguistics
(Volume 1: Long Papers),edited by Lun-Wei Ku, Andre Martins, and Vivek Srikumar,
15523–15536. ACL 2024. Bangkok, Thailand: Association for Computational Linguis-
tics, August.
39
Li, Yuan, Yixuan Zhang, and Lichao Sun. 2023. “MetaAgents: Simulating Interactions of
Human Behaviors for LLM-based T Ask-Oriented Coordination via Collaborative Gen-
erative Agents.” arXiv.org.
Liu, Xiao, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, et al. 2023.
“AgentBench: Evaluating LLMs as Agents.”International Conference on Learning Rep-
resentations.
Lopez-Lira, Alejandro, and Yuehua Tang. 2023. “Can ChatGPT Forecast Stock Price Move-
ments? Return Predictability and Large Language Models.” SSRN Electronic Journal
(April 6, 2023).
Manning, Benjamin S., Kehang Zhu, and John J. Horton. 2024. “Automated Social Science:
Language Models as Scientist and Subjects.” (Cambridge, MA) (April 29, 2024).
Molnar, Christoph. 2022. Interpretable Machine Learning.
Pelster, Matthias, and Joel Val. 2023. “Can Chatgpt Assist in Picking Stocks?”Social Science
Research Network.
Piatti, Giorgio, Zhijing Jin, Max Kleiman-Weiner, Bernhard Sch¨ olkopf, Mrinmaya Sachan,
and Rada Mihalcea. 2024. “Cooperate or Collapse: Emergence of Sustainable Coopera-
tion in a Socie Ty of LLM Agents.” arXiv.org.
Ping, Chen. 2019. “From Complexity Science to Complexity Economics.” In Alternative
Approaches to Economic Theory,19–55. Routledge, June 11, 2019.
Wang, Saizhuo, Hang Yuan, Lionel M. Ni, and Jian Guo. 2024. “QuantAgent: Seeking Holy
Grail in Trading by Self-Improving Large Lang Uage Model.” arXiv.org.
Weitzel, Utz, Christoph Huber, J¨ urgen Huber, Michael Kirchler, Florian Lindner, and Julia
Rose. 2020. “Bubbles and Financial Professionals.” The Review of Financial Studies33,
no. 6 (June 1, 2020): 2659–2696.
40
Wolfram, Elsner. 2017. “Complexity Economics as Heterodoxy: Theory and Policy.”Journal
of Economic Issues51, no. 4 (October 2, 2017): 939–978.
Woodhouse, Drew, and Alex Charlesworth. 2023. “Can ChatGPT Predict Future Interest
Rate Decisions?” Social Science Research Network.
Xie, Chengxing, Canyu Chen, Feiran Jia, Ziyu Ye, Shiyang Lai, Kai Shu, Jindong Gu, et al.
2024. “Can Large Language Model Agents Simulate Human Trust Behavior?”arXiv.org.
Yang, Stephen. 2023. “Predictive Patentomics: Forecasting Innovation Success and Valuation
w Ith ChatGPT.” Social Science Research Network.
Yu, Yangyang, Haohang Li, Zhi Chen, Yuechen Jiang, Yang Li, Denghui Zhang, Rong
Liu, Jordan W. Suchow, and Khaldoun Khashanah. 2024. “FinMem: A Performance-
Enhanced LLM Trading Agent with Layered Memory a Nd Character Design.”Proceed-
ings of the AAAI Symposium Series3, no. 1 (May 20, 2024): 595–597.
Yu, Yangyang, Zhiyuan Yao, Haohang Li, Zhiyang Deng, Yupeng Cao, Zhi Chen, Jordan W.
Suchow, et al. 2024. “FinCon: A Synthesized LLM Multi-Agent System with Conceptual
Verbal Reinforcement for Enhanced Financial Decision Making.” Pre-published, Novem-
ber 7, 2024. Accessed January 8, 2025. https://doi.org/10.48550/arXiv.2407.06567.
arXiv: 2407.06567 [cs]. http://arxiv.org/abs/2407.06567.
Zhang, Chong, Xinyi Liu, Zhongmou Zhang, Mingyu Jin, Lingyao Li, Zhenting Wang,
Wenyue Hua, et al. 2024. “When AI Meets Finance (StockAgent): Large Language
Model-based Stock Trading in Simulated Real-world Environments.” Pre-published,
September 21, 2024. Accessed January 26, 2025. https://doi.org /10.48550/arXiv .
2407.18957. arXiv: 2407.18957 [q-fin]. http://arxiv.org/abs/2407.18957.
41
A Technical Implementation Details
A.1 Agent Type Specifications
This section details the base system prompts for each agent type in our simulation. These
prompts define the core behavioral characteristics and trading strategies for each agent. Each
prompt consists of:
• A role definition that establishes the agent’s trading philosophy
• A structured trading strategy that guides decision-making""",
            """ripe for investigation using this tool include the emergence of novel trading strategies, the
precise effects of agent heterogeneity on market stability, and the development of robust
validation protocols for AI traders. As artificial intelligence becomes more integrated into
finance, collaborative research leveraging adaptable simulation environments like this one
will be crucial for understanding and responsibly shaping the future of trading.
35
References
Arthur, W. Brian. 2013. “Complexity Economics : A Different Framework for Economic
Thought.”
Babina, Tania, Anastassia Fedyk, Alex He, and James Hodson. 2024. “Artificial Intelli-
gence, Firm Growth, and Product Innovation.” Journal of Financial Economics 151
(January 1, 2024): 103745.
Balland, Pierre-Alexandre, Tom Broekel, Dario Diodato, Elisa Giuliani, Ricardo Hausmann,
Neave O’Clery, and David Rigby. 2022. “The New Paradigm of Economic Complexity.”
Research Policy51, no. 3 (April): 104450.
Bianchi, Federico, Patrick John Chia, Mert Yuksekgonul, Jacopo Tagliabue, Dan Jurafsky,
and James Zou. 2024. “How Well Can LLMs Negotiate? NegotiationArena Platform and
Analysis.” arXiv.org.
Bybee, J. Leland. 2023. “The Ghost in the Machine: Generating Beliefs with Large Language
Models.” arXiv: 2305.02823.
Campello, Murillo, Lin William Cong, and Luofeng Zhou. 2023. “AlphaManager: A Data-
Driven-Robust-Control Approach to Corporate Finance.” Pre-published, December 2,
2023. SSRN Scholarly Paper. Accessed December 22, 2024. https://doi.org/10.2139/
ssrn.4590323. Social Science Research Network: 4590323. https://papers.ssrn.com/
abstract=4590323.
Chen, Yifei, Bryan T. Kelly, and Dacheng Xiu. 2022. “Expected Returns and Large Lan-
guage Models.” Pre-published, November 22, 2022. SSRN Scholarly Paper. Accessed
January 26, 2025. Social Science Research Network: 4416687. https://papers.ssrn.com/
abstract=4416687.
36
Chen, Zihan, Lei Zheng, Chengyu Lu, Jialu Yuan, and Di Zhu. 2023. “ChatGPT Informed
Graph Neural Network for Stock Movement Prediction.” Social Science Research Net-
work.
Chuang, Yun-Shiuan, Agam Goyal, Nikunj Harlalka, Siddharth Suresh, Robert Hawkins,
Sijia Yang, Dhavan Shah, Junjie Hu, and Timothy T. Rogers. 2023. “Simulating Opin-
ion Dynamics with Networks of LLM-based Agents.” North American Chapter of the
Association for Computational Linguistic s.
Colliard, Jean-Edouard, Thierry Foucault, and Stefano Lovo. 2022. “Algorithmic Pricing
and Liquidity in Securities Markets.” Pre-published, October 18, 2022. SSRN Scholarly
Paper. Accessed April 4, 2025. https://doi.org/10.2139/ssrn.4252858. Social Science
Research Network: 4252858. https://papers.ssrn.com/abstract=4252858.
Cong, Lin William, Ke Tang, Jingyuan Wang, and Yang Zhang. 2021. “AlphaPortfolio:
Direct Construction Through Deep Reinforcement Learning and Interpretable AI.” Pre-
published, August 1, 2021. SSRN Scholarly Paper. Accessed December 22, 2024. https:
//doi.org/10.2139/ssrn.3554486. Social Science Research Network: 3554486. https:
//papers.ssrn.com/abstract=3554486.
Dou, Winston Wei, Itay Goldstein, and Yan Ji. 2024. “AI-Powered Trading, Algorithmic
Collusion, and Price Efficiency.” Pre-published, May 30, 2024. SSRN Scholarly Paper.
Accessed April 4, 2025. https://doi.org/10.2139/ssrn.4452704. Social Science Research
Network: 4452704. https://papers.ssrn.com/abstract=4452704.
Eisfeldt, Andrea L., Gregor Schubert, Miao Ben Zhang, and Bledi Taska. 2023. “Generative
AI and Firm Values.” Pre-published, May 2, 2023. SSRN Scholarly Paper. Accessed
January 26, 2025. https : / / doi .org / 10 .2139 / ssrn . 4436627. Social Science Research
Network: 4436627. https://papers.ssrn.com/abstract=4436627.
37
Gao, Shen, Yuntao Wen, Minghang Zhu, Jianing Wei, Yuhan Cheng, Qunzi Zhang, and Shuo
Shang. 2024. “Simulating Financial Market via Large Language Model Based Agents.”
Pre-published, June 28, 2024. Accessed January 26, 2025. https://doi.org/10.48550/""",
            """an open-source framework with three key components: (1) a structured protocol for im-
plementing and validating LLM trading agents, supporting both LLM-based and traditional
rule-based agents; (2) a controlled market environment with realistic microstructure for test-
ing agent interactions; and (3) a comprehensive data collection system for analyzing trading
behavior. This framework serves multiple stakeholders in preparation for the evolution of
financial markets: practitioners developing LLM-based trading systems, regulators antic-
ipating widespread LLM adoption, and researchers studying market dynamics with LLM
agents.
1.1 Related Work
This work contributes to several strands of literature. First, advancing the growing body
of research on artificial intelligence in finance by demonstrating that large language mod-
els (LLMs) can serve as effective autonomous trading agents while providing a framework
for their implementation. Second, by contributing to the market microstructure literature
by providing insights into how markets might evolve as LLM-based traders become active
participants, with implications for price formation, liquidity provision, and market stabil-
ity. Third, by contributing to experimental markets research by introducing an environment
for studying complex trading interactions, offering unprecedented control and replicability
compared to traditional human-subject experiments.
4
Recent studies have explored ChatGPT’s potential in various financial tasks. Research
shows that ChatGPT can effectively predict stock price movements using news headlines,
outperforming traditional sentiment analysis (Lopez-Lira and Tang 2023) and that forecast-
ing with its embeddings outperforms traditional sentiment analysis (Chen, Kelly, and Xiu
2022). When integrated with Graph Neural Networks, ChatGPT improves stock movement
prediction and portfolio performance (Chen et al. 2023. ChatGPT can understand Federal
Reserve communications Hansen and Kazinnik (2023). The model also can extract manage-
rial expectations from corporate disclosures, predicting future investments and returns (Jha
et al. 2025). ChatGPT-4 provides valuable investment advice with positive correlations to
subsequent earnings announcements and stock returns (Pelster and Val 2023), and it en-
hances patent value forecasts by processing patent text (Yang 2023). Moreover, ChatGPT
shows promise in central bank analysis, predicting future interest rate decisions from pol-
icy communications (Woodhouse and Charlesworth 2023). Recent work also focuses on the
effects of AI adoption by firms (Eisfeldt et al. 2023, Babina et al. 2024).
Foundational work on LLMs as economic agents demonstrates their ability to simulate
human behavior in economic contexts. Horton (2023) introduce the concept of “homo silicus”
by using LLMs as computational models of human behavior, showing that they can repli-
cate classic behavioral economics findings. Manning, Zhu, and Horton (2024) extend this
approach through automated methods for generating and testing social scientific hypotheses
with LLMs, demonstrating strong results in market contexts such as auctions. Meanwhile,
N. Li et al. (2024) show LLMs’ potential in macroeconomic simulation for consumption
and labor decisions. Recent work also shows the potential of LLMs to proxy for human
behavior in the context of surveys (Hansen et al. (2024)) or economic expectations (Bybee
(2023)). This work, however, focuses on financial markets and how LLM agents can operate
as full-fledged trading participants.
Recent research examines specific applications of LLMs for trading. FinMem and Trad-
ingGPT introduce frameworks with layered memory systems and customizable agent traits
5
to improve financial decision-making (Yu, Li, et al. 2024; Li, Zhang, and Sun 2023). Hierar-
chical multi-agent architectures have been explored in FinCon, which uses a manager-analyst""",
            """2407.18957. arXiv: 2407.18957 [q-fin]. http://arxiv.org/abs/2407.18957.
41
A Technical Implementation Details
A.1 Agent Type Specifications
This section details the base system prompts for each agent type in our simulation. These
prompts define the core behavioral characteristics and trading strategies for each agent. Each
prompt consists of:
• A role definition that establishes the agent’s trading philosophy
• A structured trading strategy that guides decision-making
• Specific instructions for when to use market orders vs limit orders
At runtime, these base prompts are combined with:
• Current market state (price, volume, order book depth)
• Position information (current holdings and available cash)
• Trading options and required response format
The standard runtime template includes:
Position Information Template
Your Position:
- Available Shares: {shares} shares (Short selling is not allowed)
- Main Cash Account: ${cash:.2f}
- Dividend Cash Account (not available for trading): ${dividend_cash:.2f}
- Total Available Cash: ${total_available_cash:.2f} (Borrowing is not allowed)
- Shares in Orders: {committed_shares} shares
- Cash in Orders: ${committed_cash:.2f}
42
Trading Options Template
Your analysis should include:
- valuation_reasoning: Your numerical analysis of the asset’s fundamental value
- valuation: Your estimate of the asset’s current fundamental value
- price_target_reasoning: Your numerical analysis of the asset’s price target
- price_target: Your predicted price for the next round
- reasoning: Your explanation for the trading decision
Trading Options:
1. New Orders (replace_decision=’Add’):
- Single or multiple orders allowed
- For each order:
- Market order: Set order_type=’market’
- Limit order: Set order_type=’limit’ and specify price_limit
- IMPORTANT: Sell orders require sufficient available shares
- Short selling is NOT allowed
2. Cancel Orders (replace_decision=’Cancel’):
- Return an empty orders list: orders=[]
Your decision must include:
- orders: list of orders (empty list for Hold/Cancel)
- For Buy/Sell orders, each must contain:
- decision: "Buy" or "Sell"
- quantity: number of shares
- order_type: "market" or "limit"
- price_limit: required for limit orders
- reasoning: brief explanation
- replace_decision: "Add", "Cancel", or "Replace"
43
Base System Prompts The following are the base system prompts for each LLM-based
agent type:
A.1.1 Value-Based Agents
Value Investor
You are a value investor who focuses on fundamental analysis.
You believe in mean reversion and try to buy undervalued assets and sell overvalued ones.
A.1.2 Trend-Following Agents
Momentum Trader
You are a momentum trader who focuses on price trends and volume.
You believe that ’the trend is your friend’ and try to identify and follow market momentum.
A.1.3 Liquidity Providers Agents
Market Maker
You are a professional market maker who provides liquidity to the market.
Your profit comes from capturing the spread between bid and ask prices, not from directional price movement.
IMPORTANT: There is NO SHORT SELLING allowed. You can only sell shares you already own.
Trading Guidelines:
- Place LIMIT buy orders slightly below the current market price (1-3% lower)
- Place LIMIT sell orders slightly above the current market price (1-3% higher)
- Your spread should be proportional to volatility but typically 2-6% of price
- NEVER place sell orders more than 10% above your buy orders
- Adjust your spread width based on recent price volatility
44
Inventory Management (No Short Selling):
- Monitor your current inventory in the market data
- Only place sell orders for quantities you actually own
- If you have no inventory, focus on buy orders first
- As you acquire inventory, gradually place sell orders
- If inventory grows too large, reduce or pause buy orders
- Adjust your buy/sell ratio based on current inventory level
Example: If price = $100, you might place buy orders at $97-99 and sell orders at $101-103,""",
        ],
    ),
    LLMTestCase(
        input="What systemic risks do the authors foresee if many firms deploy similarly prompted LLM traders in real markets?",
        actual_output="""The authors are concerned that if many trading firms use similarly prompted Large Language Model (LLM) based trading agents, it could lead to increased systemic risk in financial markets. Specifically, they highlight the risk of correlated behavior: because these agents would be built on similar underlying architectures and responding to the same market signals in similar ways (due to similar prompts), they might make the same trading decisions at the same time. This could amplify market instability, potentially causing:

Exaggerated Price Swings: If many LLMs simultaneously decide to buy or sell a particular asset, it could lead to larger-than-normal price increases or decreases, increasing market volatility.

Flash Crashes: In extreme cases, this correlated selling could create a sudden, sharp drop in prices, similar to a flash crash.

Bubble Formation and Bursting: Similarly, correlated buying by many LLMs could inflate asset bubbles, which could then burst dramatically when the LLMs decide to sell. This is especially risky because the LLMs might continue to follow their instructions even when a bubble is forming, unlike human traders who might recognize the bubble and adjust their strategy.""",
        expected_output="""If many firms deploy similarly prompted LLMs built on the same foundation model, their synchronised reactions could amplify volatility and create new instabilities.""",
        context=[
            """A key concern is the potential for widespread correlated behavior… similar underlying LLM architectures responding uniformly… could destabilize trading patterns without explicit coordination."""
        ],
        retrieval_context=[
            """2024). Another examines LLMs’ strategic capabilities through task-based simulations and
collaborative decision-making (Li, Zhang, and Sun 2023; Piatti et al. 2024).
Within the computer science literature, early works apply LLMs to financial markets but
abstract away many fundamental stock market characteristics. Often, they employ single-
price clearing mechanisms without a persistent order book, ignore partial fills and bid-ask
spreads, and omit dividends. Consequently, these simplified environments can primarily
address exogenous macro shocks (e.g., changes in interest rates or inflation; Gao et al. 2024),
exogenous policy changes (Zhang et al. 2024), or rely on advanced methods such as repetitive
next-token predictions to generate better answers (Koa et al. 2024). This work extends
these efforts by incorporating these crucial market features, enabling the study of complex
endogenous events such as flash crashes, liquidity shocks, and large-trader impacts.
This work also connects to emerging research on algorithmic and AI-powered trading
systems. Dou, Goldstein, and Ji (2024) demonstrate how reinforcement learning-based AI
speculators can autonomously learn to sustain collusive behavior without explicit coordi-
nation, achieving supra-competitive profits through either price-trigger strategies or self-
confirming bias in learning. This finding is particularly informative for this framework as
it highlights potential emergent behaviors that may arise when intelligent agents interact in
7
markets—behaviors that could manifest differently with LLM agents due to their natural
language reasoning capabilities. Similarly, Colliard, Foucault, and Lovo (2022) examine al-
gorithmic market makers using Q-learning and find they charge markups that increase when
adverse selection costs decrease—contrary to Nash equilibrium predictions. Their work pro-
vides methodological insights on how to test strategic pricing behaviors against theoretical
benchmarks incorporated into this LLM-based framework.
Finally, this approach is informed by complexity economics, which views markets as dy-
namic, non-equilibrium systems where agents adaptively learn and evolve strategies (Arthur
2013; Wolfram 2017). According to this view, markets exhibit emergent phenomena and
self-organization, especially when trading agents (human or artificial) update their behav-
ior in response to outcomes. This paradigm is particularly relevant in an era of increasing
automation and algorithmic trading (Balland et al. 2022; Ping 2019). Like adaptive agents
in complexity economics, these LLM traders incorporate new information and adjust their
strategies, generating emergent market patterns—a key motivation behind this framework.
Unlike previous frameworks that abstract away crucial market features or focus on narrow
strategies, this system incorporates realistic market microstructure while accommodating
heterogeneous agents interacting simultaneously. While earlier work demonstrates LLMs’
promise for macroeconomic modeling and simple trading simulations, this work introduces a
complex, open-source financial market platform that supports multiple agent architectures,
thorough market microstructure (limit orders, partial fills, dividends), and rigorous testing
protocols—fulfilling a critical need in complexity economics research and market microstruc-
ture analysis.
2 Methodology
The methodology section contains three parts. The first part describes the market design,
the second agents’ design, and the third the analysis module.
8
2.1 Market Design
Our methodological framework integrates three components that create a controlled envi-
ronment for LLM-based trading agents. The framework implements a flexible continuous
double-auction market mechanism that couples standard market microstructure principles
with market clearing and matching algorithms to accommodate asynchronous LLM decisions.""",
            """Can Large Language Models Trade? Testing Financial
Theories with LLM Agents in Market Simulations
Alejandro Lopez-Lira∗
First Version: November 29, 2024; Current Version: April 16, 2025
Abstract
This paper presents a realistic simulated stock market where large language models
(LLMs) act as heterogeneous competing trading agents. The open-source framework
incorporates a persistent order book with market and limit orders, partial fills, div-
idends, and equilibrium clearing alongside agents with varied strategies, information
sets, and endowments. Agents submit standardized decisions using structured outputs
and function calls while expressing their reasoning in natural language. Three findings
emerge: First, LLMs demonstrate consistent strategy adherence and can function as
value investors, momentum traders, or market makers per their instructions. Second,
market dynamics exhibit features of real financial markets, including price discovery,
bubbles, underreaction, and strategic liquidity provision. Third, the framework enables
analysis of LLMs’ responses to varying market conditions, similar to partial dependence
plots in machine-learning interpretability. The framework allows simulating financial
theories without closed-form solutions, creating experimental designs that would be
costly with human participants, and establishing how prompts can generate correlated
behaviors affecting market stability.
Keywords: LLM Agents; Agent-Based Markets; Experimental Finance; AI Trading;
Multi-Agent Systems
∗University of Florida. Email: alejandro.lopez-lira@warrington.ufl.edu. I am grateful to seminar par-
ticipants at the London Business School, Oxford University, Stockholm School of Economics, University of
Virginia, and the City University of Hong Kong for helpful suggestions and feedback.
1
arXiv:2504.10789v1  [q-fin.CP]  15 Apr 2025
1 Introduction
Large language models (LLMs) can increasingly function as autonomous agents—systems
that observe, reason, and act independently. LLMs have shown promising results in finan-
cial forecasting, but their potential as trading agents introduces a fundamental shift from
algorithms with explicit objectives to systems guided by natural language instructions. This
change raises critical questions: Can LLMs execute trading strategies? Do LLMs optimize
for profit maximization? What are the implications for market stability and efficiency?
If LLMs trade similarly to humans, they could enable experimental market simulations
without human participants. Conversely, if their trading behavior differs, understanding
these differences becomes critical for systemic risk management. These questions extend be-
yond theory; LLM-based strategies are already being deployed.1 To address these questions,
I develop an open-source simulation that tests LLM trading agents in a realistic market envi-
ronment with a persistent order book, supporting various order types, stochastic dividends,
and heterogeneous information.
The framework allows heterogeneous LLMs—defined in natural language, using different
system prompts—to act as diverse types of traders, such as value investors, momentum
traders, market makers, and contrarians. Agents submit standardized trading decisions in a
human-readable format while expressing their reasoning transparently. Figure 1 illustrates
this approach, showing how a speculator agent combines explicit valuation reasoning with
structured trading parameters, enabling systematic analysis and insight into the agent’s
decision-making process.
The analysis reveals three key findings about LLMs’ capabilities as trading agents. First,
LLMs can effectively execute trading strategies. They consistently understand market me-
chanics, process market information, form price expectations, and execute trades according
to specific instructions. Their trading behavior is highly sensitive to the prompts they
receive—they faithfully follow directions regardless of profit implications. This observance""",
            """ripe for investigation using this tool include the emergence of novel trading strategies, the
precise effects of agent heterogeneity on market stability, and the development of robust
validation protocols for AI traders. As artificial intelligence becomes more integrated into
finance, collaborative research leveraging adaptable simulation environments like this one
will be crucial for understanding and responsibly shaping the future of trading.
35
References
Arthur, W. Brian. 2013. “Complexity Economics : A Different Framework for Economic
Thought.”
Babina, Tania, Anastassia Fedyk, Alex He, and James Hodson. 2024. “Artificial Intelli-
gence, Firm Growth, and Product Innovation.” Journal of Financial Economics 151
(January 1, 2024): 103745.
Balland, Pierre-Alexandre, Tom Broekel, Dario Diodato, Elisa Giuliani, Ricardo Hausmann,
Neave O’Clery, and David Rigby. 2022. “The New Paradigm of Economic Complexity.”
Research Policy51, no. 3 (April): 104450.
Bianchi, Federico, Patrick John Chia, Mert Yuksekgonul, Jacopo Tagliabue, Dan Jurafsky,
and James Zou. 2024. “How Well Can LLMs Negotiate? NegotiationArena Platform and
Analysis.” arXiv.org.
Bybee, J. Leland. 2023. “The Ghost in the Machine: Generating Beliefs with Large Language
Models.” arXiv: 2305.02823.
Campello, Murillo, Lin William Cong, and Luofeng Zhou. 2023. “AlphaManager: A Data-
Driven-Robust-Control Approach to Corporate Finance.” Pre-published, December 2,
2023. SSRN Scholarly Paper. Accessed December 22, 2024. https://doi.org/10.2139/
ssrn.4590323. Social Science Research Network: 4590323. https://papers.ssrn.com/
abstract=4590323.
Chen, Yifei, Bryan T. Kelly, and Dacheng Xiu. 2022. “Expected Returns and Large Lan-
guage Models.” Pre-published, November 22, 2022. SSRN Scholarly Paper. Accessed
January 26, 2025. Social Science Research Network: 4416687. https://papers.ssrn.com/
abstract=4416687.
36
Chen, Zihan, Lei Zheng, Chengyu Lu, Jialu Yuan, and Di Zhu. 2023. “ChatGPT Informed
Graph Neural Network for Stock Movement Prediction.” Social Science Research Net-
work.
Chuang, Yun-Shiuan, Agam Goyal, Nikunj Harlalka, Siddharth Suresh, Robert Hawkins,
Sijia Yang, Dhavan Shah, Junjie Hu, and Timothy T. Rogers. 2023. “Simulating Opin-
ion Dynamics with Networks of LLM-based Agents.” North American Chapter of the
Association for Computational Linguistic s.
Colliard, Jean-Edouard, Thierry Foucault, and Stefano Lovo. 2022. “Algorithmic Pricing
and Liquidity in Securities Markets.” Pre-published, October 18, 2022. SSRN Scholarly
Paper. Accessed April 4, 2025. https://doi.org/10.2139/ssrn.4252858. Social Science
Research Network: 4252858. https://papers.ssrn.com/abstract=4252858.
Cong, Lin William, Ke Tang, Jingyuan Wang, and Yang Zhang. 2021. “AlphaPortfolio:
Direct Construction Through Deep Reinforcement Learning and Interpretable AI.” Pre-
published, August 1, 2021. SSRN Scholarly Paper. Accessed December 22, 2024. https:
//doi.org/10.2139/ssrn.3554486. Social Science Research Network: 3554486. https:
//papers.ssrn.com/abstract=3554486.
Dou, Winston Wei, Itay Goldstein, and Yan Ji. 2024. “AI-Powered Trading, Algorithmic
Collusion, and Price Efficiency.” Pre-published, May 30, 2024. SSRN Scholarly Paper.
Accessed April 4, 2025. https://doi.org/10.2139/ssrn.4452704. Social Science Research
Network: 4452704. https://papers.ssrn.com/abstract=4452704.
Eisfeldt, Andrea L., Gregor Schubert, Miao Ben Zhang, and Bledi Taska. 2023. “Generative
AI and Firm Values.” Pre-published, May 2, 2023. SSRN Scholarly Paper. Accessed
January 26, 2025. https : / / doi .org / 10 .2139 / ssrn . 4436627. Social Science Research
Network: 4436627. https://papers.ssrn.com/abstract=4436627.
37
Gao, Shen, Yuntao Wen, Minghang Zhu, Jianing Wei, Yuhan Cheng, Qunzi Zhang, and Shuo
Shang. 2024. “Simulating Financial Market via Large Language Model Based Agents.”
Pre-published, June 28, 2024. Accessed January 26, 2025. https://doi.org/10.48550/""",
            """33
ants, allowing researchers to study how different belief structures influence price formation
and trading patterns under different initial mispricings. In these scenarios, the fundamental
price is hidden from agents, forcing them to rely on their own valuation models.
3.2.5 Market Stress
This scenario tests market resilience under challenging conditions by creating a more volatile
environment. The scenario includes two consistently bullish Optimistic traders, two consis-
tently bearish Pessimistic traders, two Market makers (liquidity providers), and two Value
investors (rational benchmark traders). The scenario runs for 100 rounds to study long-term
market behavior and includes unequal initial endowments, with optimistic traders having
more cash (1.5x baseline) but fewer shares (0.5x baseline) and pessimistic traders having less
cash (0.5x baseline) but more shares (1.5x baseline). This resource imbalance tests whether
particular agent types can dominate market outcomes through resource advantages.
The scenarios presented here demonstrate the framework’s capabilities for exploring di-
verse market conditions. Its modular structure facilitates the straightforward definition and
implementation of alternative experimental designs, enabling researchers to tailor simulations
to specific research questions.
In all scenarios, we maintain consistent baseline parameters with a fundamental value
of $28.00, calculated from the expected dividend of $1.40 and interest rate of 5%. Agent
endowments start at 1,000,000 monetary units and 10,000 shares unless specifically modified.
Transaction costs are set to zero to isolate the effects of agent behavior and market structure
on price formation.
4 Conclusion
This paper demonstrates that Large Language Models can effectively function as diverse
trading agents—from value investors to market makers—maintaining strategic consistency
34
while adapting to market conditions. Our experimental framework reveals that their in-
teractions generate realistic market dynamics, including phenomena like price bubbles and
corrections, highlighting both the capabilities and potential risks of deploying LLM agents
in financial markets.
These findings carry significant implications for market structure and regulation. While
LLM agents can enhance price discovery and liquidity, their adherence to programmed strate-
gies, even potentially flawed ones derived from prompts, could amplify market volatility or
introduce novel systemic risks, as observed in our simulated bubble scenarios. A key concern
is the potential for widespread correlated behavior: similar underlying LLM architectures
responding uniformly to comparable prompts or market signals could inadvertently create
destabilizing trading patterns without explicit coordination. This underscores the critical
need for rigorous testing and validation of LLM-based trading systems prior to live deploy-
ment.
A central contribution of this work is the open-source simulation framework itself, de-
signed to catalyze research into LLM trading agents. We invite the research community to
utilize and extend this platform to investigate pressing questions in this rapidly evolving
area. The framework enables systematic exploration of complex scenarios—such as hybrid
human-LLM markets, stress tests, varying market structures, regulatory impacts, and the
nuances of LLM prompting—often difficult or costly to study otherwise. Specific avenues
ripe for investigation using this tool include the emergence of novel trading strategies, the
precise effects of agent heterogeneity on market stability, and the development of robust
validation protocols for AI traders. As artificial intelligence becomes more integrated into
finance, collaborative research leveraging adaptable simulation environments like this one
will be crucial for understanding and responsibly shaping the future of trading.
35
References""",
            """(2023)). This work, however, focuses on financial markets and how LLM agents can operate
as full-fledged trading participants.
Recent research examines specific applications of LLMs for trading. FinMem and Trad-
ingGPT introduce frameworks with layered memory systems and customizable agent traits
5
to improve financial decision-making (Yu, Li, et al. 2024; Li, Zhang, and Sun 2023). Hierar-
chical multi-agent architectures have been explored in FinCon, which uses a manager-analyst
setup for collaborative portfolio decisions (Yu, Yao, et al. 2024). QuantAgent implements
a self-improving signal-mining approach (Wang et al. 2024), while other work underscores
the importance of long-term memory in LLM agents via vector databases (Hatalis et al.
2024). This line of research builds on successful reinforcement learning applications such as
AlphaPortfolio (Cong et al. 2021) and AlphaManager (Campello, Cong, and Zhou 2023),
which leverage deep RL and robust control for portfolio management.
Analyzing LLM agent behavior by changing only some parameters draws on methods
from the interpretable machine learning literature. In particular, the systematic variation
of market parameters to reveal decision patterns mirrors partial dependence plots and in-
dividual conditional expectation curves used to interpret complex machine learning models
(Molnar 2022). These techniques help reveal how LLM agents respond to changes in specific
variables while holding others constant, providing insight into their internal decision-making
processes that would otherwise remain opaque.
Beyond finance, studies of LLM capabilities in interactive or multi-agent settings offer
valuable insights. Benchmarks like AgentBench evaluate LLMs’ performance in interac-
tive tasks (Liu et al. 2023), while InvestorBench focuses on financial decision-making tasks
specifically (H. Li et al. 2024). NegotiationArena demonstrates LLMs’ capacity for strategic
interaction in bargaining contexts (Bianchi et al. 2024). Similarly, Guo et al. (2024) provide
an economics ”arena” where LLMs compete in strategic games, revealing that advanced
models like GPT-4 can exhibit rational, adaptive behavior—albeit not always reaching Nash
Equilibrium. Existing frameworks typically assess individual agents or hierarchical collab-
orations, whereas this work studies emergent market behaviors that arise from multiple
independent LLM traders interacting in a marketplace.
The approach also connects to the tradition of experimental asset markets. For instance,
Weitzel et al. (2020) show that even finance professionals are susceptible to speculative
6
bubbles, especially amid high capital inflows. Kop´ anyi-Peuker and Weber (2021) find that
trading experience alone does not eliminate bubbles, challenging assumptions about rational
market learning. Kirchler, Huber, and St¨ ockl (2012) identify confusion about fundamental
values as a key driver of bubble formation. This framework offers a new way to study these
phenomena with LLM traders, which can be rigorously parameterized for sophistication,
strategy, and information processing. Hence, this paper provides a method to investigate
how automated or ”artificial” agents might affect market stability or volatility.
Other recent work highlights the versatility of LLM agents in complex, interactive sce-
narios beyond finance. One stream focuses on simulating social behaviors—such as opinion
dynamics (Chuang et al. 2023), trust (Xie et al. 2024), and resource-sharing (Piatti et al.
2024). Another examines LLMs’ strategic capabilities through task-based simulations and
collaborative decision-making (Li, Zhang, and Sun 2023; Piatti et al. 2024).
Within the computer science literature, early works apply LLMs to financial markets but
abstract away many fundamental stock market characteristics. Often, they employ single-
price clearing mechanisms without a persistent order book, ignore partial fills and bid-ask""",
            """ceedings of the 62nd Annual Meeting of the Association for Computational Linguistics
(Volume 1: Long Papers),edited by Lun-Wei Ku, Andre Martins, and Vivek Srikumar,
15523–15536. ACL 2024. Bangkok, Thailand: Association for Computational Linguis-
tics, August.
39
Li, Yuan, Yixuan Zhang, and Lichao Sun. 2023. “MetaAgents: Simulating Interactions of
Human Behaviors for LLM-based T Ask-Oriented Coordination via Collaborative Gen-
erative Agents.” arXiv.org.
Liu, Xiao, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, et al. 2023.
“AgentBench: Evaluating LLMs as Agents.”International Conference on Learning Rep-
resentations.
Lopez-Lira, Alejandro, and Yuehua Tang. 2023. “Can ChatGPT Forecast Stock Price Move-
ments? Return Predictability and Large Language Models.” SSRN Electronic Journal
(April 6, 2023).
Manning, Benjamin S., Kehang Zhu, and John J. Horton. 2024. “Automated Social Science:
Language Models as Scientist and Subjects.” (Cambridge, MA) (April 29, 2024).
Molnar, Christoph. 2022. Interpretable Machine Learning.
Pelster, Matthias, and Joel Val. 2023. “Can Chatgpt Assist in Picking Stocks?”Social Science
Research Network.
Piatti, Giorgio, Zhijing Jin, Max Kleiman-Weiner, Bernhard Sch¨ olkopf, Mrinmaya Sachan,
and Rada Mihalcea. 2024. “Cooperate or Collapse: Emergence of Sustainable Coopera-
tion in a Socie Ty of LLM Agents.” arXiv.org.
Ping, Chen. 2019. “From Complexity Science to Complexity Economics.” In Alternative
Approaches to Economic Theory,19–55. Routledge, June 11, 2019.
Wang, Saizhuo, Hang Yuan, Lionel M. Ni, and Jian Guo. 2024. “QuantAgent: Seeking Holy
Grail in Trading by Self-Improving Large Lang Uage Model.” arXiv.org.
Weitzel, Utz, Christoph Huber, J¨ urgen Huber, Michael Kirchler, Florian Lindner, and Julia
Rose. 2020. “Bubbles and Financial Professionals.” The Review of Financial Studies33,
no. 6 (June 1, 2020): 2659–2696.
40
Wolfram, Elsner. 2017. “Complexity Economics as Heterodoxy: Theory and Policy.”Journal
of Economic Issues51, no. 4 (October 2, 2017): 939–978.
Woodhouse, Drew, and Alex Charlesworth. 2023. “Can ChatGPT Predict Future Interest
Rate Decisions?” Social Science Research Network.
Xie, Chengxing, Canyu Chen, Feiran Jia, Ziyu Ye, Shiyang Lai, Kai Shu, Jindong Gu, et al.
2024. “Can Large Language Model Agents Simulate Human Trust Behavior?”arXiv.org.
Yang, Stephen. 2023. “Predictive Patentomics: Forecasting Innovation Success and Valuation
w Ith ChatGPT.” Social Science Research Network.
Yu, Yangyang, Haohang Li, Zhi Chen, Yuechen Jiang, Yang Li, Denghui Zhang, Rong
Liu, Jordan W. Suchow, and Khaldoun Khashanah. 2024. “FinMem: A Performance-
Enhanced LLM Trading Agent with Layered Memory a Nd Character Design.”Proceed-
ings of the AAAI Symposium Series3, no. 1 (May 20, 2024): 595–597.
Yu, Yangyang, Zhiyuan Yao, Haohang Li, Zhiyang Deng, Yupeng Cao, Zhi Chen, Jordan W.
Suchow, et al. 2024. “FinCon: A Synthesized LLM Multi-Agent System with Conceptual
Verbal Reinforcement for Enhanced Financial Decision Making.” Pre-published, Novem-
ber 7, 2024. Accessed January 8, 2025. https://doi.org/10.48550/arXiv.2407.06567.
arXiv: 2407.06567 [cs]. http://arxiv.org/abs/2407.06567.
Zhang, Chong, Xinyi Liu, Zhongmou Zhang, Mingyu Jin, Lingyao Li, Zhenting Wang,
Wenyue Hua, et al. 2024. “When AI Meets Finance (StockAgent): Large Language
Model-based Stock Trading in Simulated Real-world Environments.” Pre-published,
September 21, 2024. Accessed January 26, 2025. https://doi.org /10.48550/arXiv .
2407.18957. arXiv: 2407.18957 [q-fin]. http://arxiv.org/abs/2407.18957.
41
A Technical Implementation Details
A.1 Agent Type Specifications
This section details the base system prompts for each agent type in our simulation. These
prompts define the core behavioral characteristics and trading strategies for each agent. Each
prompt consists of:
• A role definition that establishes the agent’s trading philosophy
• A structured trading strategy that guides decision-making""",
            """an open-source framework with three key components: (1) a structured protocol for im-
plementing and validating LLM trading agents, supporting both LLM-based and traditional
rule-based agents; (2) a controlled market environment with realistic microstructure for test-
ing agent interactions; and (3) a comprehensive data collection system for analyzing trading
behavior. This framework serves multiple stakeholders in preparation for the evolution of
financial markets: practitioners developing LLM-based trading systems, regulators antic-
ipating widespread LLM adoption, and researchers studying market dynamics with LLM
agents.
1.1 Related Work
This work contributes to several strands of literature. First, advancing the growing body
of research on artificial intelligence in finance by demonstrating that large language mod-
els (LLMs) can serve as effective autonomous trading agents while providing a framework
for their implementation. Second, by contributing to the market microstructure literature
by providing insights into how markets might evolve as LLM-based traders become active
participants, with implications for price formation, liquidity provision, and market stabil-
ity. Third, by contributing to experimental markets research by introducing an environment
for studying complex trading interactions, offering unprecedented control and replicability
compared to traditional human-subject experiments.
4
Recent studies have explored ChatGPT’s potential in various financial tasks. Research
shows that ChatGPT can effectively predict stock price movements using news headlines,
outperforming traditional sentiment analysis (Lopez-Lira and Tang 2023) and that forecast-
ing with its embeddings outperforms traditional sentiment analysis (Chen, Kelly, and Xiu
2022). When integrated with Graph Neural Networks, ChatGPT improves stock movement
prediction and portfolio performance (Chen et al. 2023. ChatGPT can understand Federal
Reserve communications Hansen and Kazinnik (2023). The model also can extract manage-
rial expectations from corporate disclosures, predicting future investments and returns (Jha
et al. 2025). ChatGPT-4 provides valuable investment advice with positive correlations to
subsequent earnings announcements and stock returns (Pelster and Val 2023), and it en-
hances patent value forecasts by processing patent text (Yang 2023). Moreover, ChatGPT
shows promise in central bank analysis, predicting future interest rate decisions from pol-
icy communications (Woodhouse and Charlesworth 2023). Recent work also focuses on the
effects of AI adoption by firms (Eisfeldt et al. 2023, Babina et al. 2024).
Foundational work on LLMs as economic agents demonstrates their ability to simulate
human behavior in economic contexts. Horton (2023) introduce the concept of “homo silicus”
by using LLMs as computational models of human behavior, showing that they can repli-
cate classic behavioral economics findings. Manning, Zhu, and Horton (2024) extend this
approach through automated methods for generating and testing social scientific hypotheses
with LLMs, demonstrating strong results in market contexts such as auctions. Meanwhile,
N. Li et al. (2024) show LLMs’ potential in macroeconomic simulation for consumption
and labor decisions. Recent work also shows the potential of LLMs to proxy for human
behavior in the context of surveys (Hansen et al. (2024)) or economic expectations (Bybee
(2023)). This work, however, focuses on financial markets and how LLM agents can operate
as full-fledged trading participants.
Recent research examines specific applications of LLMs for trading. FinMem and Trad-
ingGPT introduce frameworks with layered memory systems and customizable agent traits
5
to improve financial decision-making (Yu, Li, et al. 2024; Li, Zhang, and Sun 2023). Hierar-
chical multi-agent architectures have been explored in FinCon, which uses a manager-analyst""",
            """decision-making process.
The analysis reveals three key findings about LLMs’ capabilities as trading agents. First,
LLMs can effectively execute trading strategies. They consistently understand market me-
chanics, process market information, form price expectations, and execute trades according
to specific instructions. Their trading behavior is highly sensitive to the prompts they
receive—they faithfully follow directions regardless of profit implications. This observance
1. For example, Autopilot has a ChatGPT-based portfolio https://x.com/thegptinvestor.
2
{"valuation_reasoning":
"The fundamental value is based on the expected dividend,
and the interest rate.
The expected dividend is $1.40, and the interest rate is 5%.
Using a perpetuity formula, the value is $1.40 / 0.05 = $28.",
"valuation":28.0,
"price_target_reasoning":"The current price is $29.00, which is
slightly above the fundamental value of $28.00. I expect the price
to remain around $29.00 in the next round due to market stability.",
"price_target":29.0,
"orders":[{"decision":"Sell","quantity":1000,"order_type":"limit",
"price_limit":29.50}],
"replace_decision":"Add",
"reasoning":"The current price is slightly above the fundamental value.
I will place a limit sell order at $29.50 to capitalize on potential price
increases."}
Figure 1: Example of a structured trading decision from a Speculator agent defined by its
system prompt: “You are a speculator who tries to profit from market inefficiencies.”. The
LLM provides explicit reasoning for its valuation, price target, and trading decision in a
machine-readable JSON format that can be directly processed by the trading system.
highlights a fundamental difference from human traders: LLMs do not inherently optimize
for profit maximization but rather for following instructions accurately.
Second, LLMs react meaningfully to market dynamics. They consider current and his-
torical prices, dividends, and other market information when making decisions. However,
they maintain their strategic direction even when market conditions change, following their
instructions even if doing so results in financial losses. This combination of responsiveness
to market conditions while maintaining strategic consistency creates a unique trading profile
distinct from rule-based algorithms and human traders.
Third, market dynamics with LLM agents can resemble actual markets and mirror classic
results from the theoretical finance literature. When these agents interact, they produce
realistic price discovery and liquidity provision with emergent behaviors, including price
convergence toward fundamental values. Depending on the distribution of agent types,
the system can generate various market phenomena, such as bubbles or underreactions to
information. This complex behavior suggests potential applications for studying market
3
dynamics using LLM agents instead of experiments with human participants.
Hence, these findings raise important questions about algorithmic consistency in LLM-
based systems. Since trading agents are implemented through prompts, their behavior in-
herits characteristics of the underlying language models. The standardization of LLM ar-
chitectures across implementations could create unexpected behavioral patterns—if many
agents are based on similar foundation models, they might exhibit correlated responses to
specific market conditions, potentially amplifying market instabilities.
To enable this analysis and accelerate development in this emerging field, we provide
an open-source framework with three key components: (1) a structured protocol for im-
plementing and validating LLM trading agents, supporting both LLM-based and traditional
rule-based agents; (2) a controlled market environment with realistic microstructure for test-
ing agent interactions; and (3) a comprehensive data collection system for analyzing trading
behavior. This framework serves multiple stakeholders in preparation for the evolution of""",
        ],
    ),
    LLMTestCase(
        input="In SRCNN, what practical role does the non‑linear mapping layer with 1 × 1 filters play in the overall SR pipeline?",
        actual_output="The non-linear mapping layer in SRCNN, which uses 1x1 filters, essentially acts as a feature selector and combiner within the super-resolution pipeline. Think of the initial layer as extracting a set of features from the low-resolution image. This second layer then takes these features and recombines them in non-linear ways to create a more informative and refined set of features. While 1x1 convolutions don't change the spatial dimensions, they allow the network to learn complex relationships between the different feature maps (different aspects of the visual information) extracted by the first layer. This step is crucial for capturing the intricate details needed to reconstruct a high-resolution image. The ReLU (Rectified Linear Unit, a function that replaces negative values with zero) activation further enhances this non-linearity, adding another level of expressiveness to the model.",
        expected_output="""It transforms every patch‑level feature vector (extracted by the first conv layer) into a new, lower‑dimensional representation that will later be linearly combined into HR pixels. Because the spatial kernel is 1 × 1, the mapping is applied channel‑wise without mixing spatial positions, mimicking the sparse‑coding step but in a single feed‑forward pass.""",
        context=[
            """The first layer extracts an n₁‑dimensional feature for each patch. In the second operation, we **map each of these n₁‑dimensional vectors into an n₂‑dimensional one. This is equivalent to applying n₂ filters which have a trivial spatial support 1 × 1 … This operation non‑linearly maps each high‑dimensional vector onto another high‑dimensional vector."""
        ],
        retrieval_context=[
            """In this paper, we show that the aforementioned
pipeline is equivalent to a deep convolutional neural net-
work [27] (more details in Section 3.2). Motivated by this
fact, we consider a convolutional neural network that
directly learns an end-to-end mapping between low- and
high-resolution images. Our method differs fundamen-
tally from existing external example-based approaches,
in that ours does not explicitly learn the dictionaries [41],
[49], [50] or manifolds [2], [4] for modeling the patch
space. These are implicitly achieved via hidden layers.
Furthermore, the patch extraction and aggregation are
also formulated as convolutional layers, so are involved
in the optimization. In our method, the entire SR pipeline
is fully obtained through learning, with little pre/post-
processing.
We name the proposed model Super-Resolution Con-
volutional Neural Network (SRCNN) 1. The proposed
SRCNN has several appealing properties. First, its struc-
ture is intentionally designed with simplicity in mind,
and yet provides superior accuracy 2 compared with
state-of-the-art example-based methods. Figure 1 shows
a comparison on an example. Second, with moderate
1. The implementation is available at http://mmlab.ie.cuhk.edu.hk/
projects/SRCNN.html.
2. Numerical evaluations by using different metrics such as the Peak
Signal-to-Noise Ratio (PSNR), structure similarity index (SSIM) [43],
multi-scale SSIM [44], information ﬁdelity criterion [38], when the
ground truth images are available.
arXiv:1501.00092v3  [cs.CV]  31 Jul 2015
2
Bicubic / 24.04 dB
SC / 25.58 dBSRCNN / 27.95 dB
Original / PSNR
2 4 6 8 10 12x 108
29.5
30
30.5
31
31.5
32
32.5
33
Number of backprops
Average test PSNR (dB)
SRCNN
SC
Bicubic
Bicubic / 24.04 dB
SC / 25.58 dBSRCNN / 27.95 dB
Original / PSNR
Bicubic / 24.04 dB
SC / 25.58 dBSRCNN / 27.95 dB
Original / PSNR
SRCNN
SC
Bicubic
Bicubic / 24.04 dB
SC / 25.58 dBSRCNN / 27.95 dB
Original / PSNR
Number of backprops
Average test PSNR (dB)
Fig. 1. The proposed Super-Resolution Convolutional
Neural Network (SRCNN) surpasses the bicubic baseline
with just a few training iterations, and outperforms the
sparse-coding-based method (SC) [50] with moderate
training. The performance may be further improved with
more training iterations. More details are provided in
Section 4.4.1 (the Set5 dataset with an upscaling factor
3). The proposed method provides visually appealing
reconstructed image.
numbers of ﬁlters and layers, our method achieves
fast speed for practical on-line usage even on a CPU.
Our method is faster than a number of example-based
methods, because it is fully feed-forward and does
not need to solve any optimization problem on usage.
Third, experiments show that the restoration quality of
the network can be further improved when (i) larger
and more diverse datasets are available, and/or (ii)
a larger and deeper model is used. On the contrary,
larger datasets/models can present challenges for exist-
ing example-based methods. Furthermore, the proposed
network can cope with three channels of color images
simultaneously to achieve improved super-resolution
performance.
Overall, the contributions of this study are mainly in
three aspects:
1) We present a fully convolutional neural net-
work for image super-resolution. The network di-
rectly learns an end-to-end mapping between low-
and high-resolution images, with little pre/post-
processing beyond the optimization.
2) We establish a relationship between our deep-
learning-based SR method and the traditional
sparse-coding-based SR methods. This relationship
provides a guidance for the design of the network
structure.
3) We demonstrate that deep learning is useful in
the classical computer vision problem of super-
resolution, and can achieve good quality and
speed.
A preliminary version of this work was presented
earlier [11]. The present work adds to the initial version
in signiﬁcant ways. Firstly, we improve the SRCNN by
introducing larger ﬁlter size in the non-linear mapping""",
            """the ﬁnal full image. The averaging can be considered
as a pre-deﬁned ﬁlter on a set of feature maps (where
each position is the “ﬂattened” vector form of a high-
resolution patch). Motivated by this, we deﬁne a convo-
lutional layer to produce the ﬁnal high-resolution image:
F(Y) = W3 ∗F2(Y) + B3. (3)
4. The ReLU can be equivalently considered as a part of the second
operation (Non-linear mapping), and the ﬁrst operation (Patch extrac-
tion and representation) becomes purely linear convolution.
Here W3 corresponds to c ﬁlters of a size n2 ×f3 ×f3,
and B3 is a c-dimensional vector.
If the representations of the high-resolution patches
are in the image domain (i.e.,we can simply reshape each
representation to form the patch), we expect that the
ﬁlters act like an averaging ﬁlter; if the representations
of the high-resolution patches are in some other domains
(e.g.,coefﬁcients in terms of some bases), we expect that
W3 behaves like ﬁrst projecting the coefﬁcients onto the
image domain and then averaging. In either way, W3 is
a set of linear ﬁlters.
Interestingly, although the above three operations are
motivated by different intuitions, they all lead to the
same form as a convolutional layer. We put all three
operations together and form a convolutional neural
network (Figure 2). In this model, all the ﬁltering weights
and biases are to be optimized. Despite the succinctness
of the overall structure, our SRCNN model is carefully
developed by drawing extensive experience resulted
from signiﬁcant progresses in super-resolution [49], [50].
We detail the relationship in the next section.
3.2 Relationship to Sparse-Coding-Based Methods
We show that the sparse-coding-based SR methods [49],
[50] can be viewed as a convolutional neural network.
Figure 3 shows an illustration.
In the sparse-coding-based methods, let us consider
that an f1 ×f1 low-resolution patch is extracted from
the input image. Then the sparse coding solver, like
Feature-Sign [29], will ﬁrst project the patch onto a (low-
resolution) dictionary. If the dictionary size is n1, this
is equivalent to applying n1 linear ﬁlters ( f1 ×f1) on
the input image (the mean subtraction is also a linear
operation so can be absorbed). This is illustrated as the
left part of Figure 3.
The sparse coding solver will then iteratively process
the n1 coefﬁcients. The outputs of this solver are n2
coefﬁcients, and usually n2 = n1 in the case of sparse
coding. These n2 coefﬁcients are the representation of
the high-resolution patch. In this sense, the sparse coding
5
responses
of patch of
neighbouring
patches
 Patch extraction
and representation
Non-linear
 mapping
Reconstruction
Fig. 3. An illustration of sparse-coding-based methods in the view of a convolutional neural network.
solver behaves as a special case of a non-linear mapping
operator, whose spatial support is 1 ×1. See the middle
part of Figure 3. However, the sparse coding solver is
not feed-forward, i.e.,it is an iterative algorithm. On the
contrary, our non-linear operator is fully feed-forward
and can be computed efﬁciently. If we set f2 = 1, then
our non-linear operator can be considered as a pixel-wise
fully-connected layer. It is worth noting that “the sparse
coding solver” in SRCNN refers to the ﬁrst two layers,
but not just the second layer or the activation function
(ReLU). Thus the nonlinear operation in SRCNN is also
well optimized through the learning process.
The above n2 coefﬁcients (after sparse coding) are
then projected onto another (high-resolution) dictionary
to produce a high-resolution patch. The overlapping
high-resolution patches are then averaged. As discussed
above, this is equivalent to linear convolutions on the
n2 feature maps. If the high-resolution patches used for
reconstruction are of size f3 ×f3, then the linear ﬁlters
have an equivalent spatial support of size f3 ×f3. See
the right part of Figure 3.
The above discussion shows that the sparse-coding-""",
            """only on the luminance channel. There are also works
attempting to super-resolve all channels simultaneously.
For example, Kim and Kwon [25] and Dai et al.[7] apply
their model to each RGB channel and combined them to
produce the ﬁnal results. However, none of them has
analyzed the SR performance of different channels, and
the necessity of recovering all three channels.
2.2 Convolutional Neural Networks
Convolutional neural networks (CNN) date back
decades [27] and deep CNNs have recently shown an
explosive popularity partially due to its success in image
classiﬁcation [18], [26]. They have also been success-
fully applied to other computer vision ﬁelds, such as
object detection [34], [40], [52], face recognition [39], and
pedestrian detection [35]. Several factors are of central
importance in this progress: (i) the efﬁcient training
implementation on modern powerful GPUs [26], (ii) the
proposal of the Rectiﬁed Linear Unit (ReLU) [33] which
makes convergence much faster while still presents good
quality [26], and (iii) the easy access to an abundance of
data (like ImageNet [9]) for training larger models. Our
method also beneﬁts from these progresses.
2.3 Deep Learning for Image Restoration
There have been a few studies of using deep learning
techniques for image restoration. The multi-layer per-
ceptron (MLP), whose all layers are fully-connected (in
contrast to convolutional), is applied for natural image
denoising [3] and post-deblurring denoising [36]. More
closely related to our work, the convolutional neural net-
work is applied for natural image denoising [22] and re-
moving noisy patterns (dirt/rain) [12]. These restoration
problems are more or less denoising-driven. Cui et al.[5]
propose to embed auto-encoder networks in their super-
resolution pipeline under the notion internal example-
based approach [16]. The deep model is not speciﬁcally
designed to be an end-to-end solution, since each layer
of the cascade requires independent optimization of the
self-similarity search process and the auto-encoder. On
the contrary, the proposed SRCNN optimizes an end-to-
end mapping. Further, the SRCNN is faster at speed. It
is not only a quantitatively superior method, but also a
practically useful one.
3 C ONVOLUTIONAL NEURAL NETWORKS FOR
SUPER -RESOLUTION
3.1 Formulation
Consider a single low-resolution image, we ﬁrst upscale
it to the desired size using bicubic interpolation, which
is the only pre-processing we perform 3. Let us denote
the interpolated image as Y. Our goal is to recover
from Y an image F(Y) that is as similar as possible
to the ground truth high-resolution image X. For the
ease of presentation, we still call Y a “low-resolution”
image, although it has the same size as X. We wish to
learn a mapping F, which conceptually consists of three
operations:
1) Patch extraction and representation: this opera-
tion extracts (overlapping) patches from the low-
resolution image Y and represents each patch as a
high-dimensional vector. These vectors comprise a
set of feature maps, of which the number equals to
the dimensionality of the vectors.
2) Non-linear mapping: this operation nonlinearly
maps each high-dimensional vector onto another
high-dimensional vector. Each mapped vector is
conceptually the representation of a high-resolution
patch. These vectors comprise another set of feature
maps.
3) Reconstruction: this operation aggregates the
above high-resolution patch-wise representations
to generate the ﬁnal high-resolution image. This
image is expected to be similar to the ground truth
X.
We will show that all these operations form a convolu-
tional neural network. An overview of the network is
depicted in Figure 2. Next we detail our deﬁnition of
each operation.
3.1.1 Patch extraction and representation
A popular strategy in image restoration ( e.g., [1]) is to
densely extract patches and then represent them by a set
of pre-trained bases such as PCA, DCT, Haar, etc. This""",
            """sparse-coding-based SR methods. This relationship
provides a guidance for the design of the network
structure.
3) We demonstrate that deep learning is useful in
the classical computer vision problem of super-
resolution, and can achieve good quality and
speed.
A preliminary version of this work was presented
earlier [11]. The present work adds to the initial version
in signiﬁcant ways. Firstly, we improve the SRCNN by
introducing larger ﬁlter size in the non-linear mapping
layer, and explore deeper structures by adding non-
linear mapping layers. Secondly, we extend the SRCNN
to process three color channels (either in YCbCr or RGB
color space) simultaneously. Experimentally, we demon-
strate that performance can be improved in comparison
to the single-channel network. Thirdly, considerable new
analyses and intuitive explanations are added to the
initial results. We also extend the original experiments
from Set5 [2] and Set14 [51] test images to BSD200 [32]
(200 test images). In addition, we compare with a num-
ber of recently published methods and conﬁrm that
our model still outperforms existing approaches using
different evaluation metrics.
2 R ELATED WORK
2.1 Image Super-Resolution
According to the image priors, single-image super res-
olution algorithms can be categorized into four types –
prediction models, edge based methods, image statistical
methods and patch based (or example-based) methods.
These methods have been thoroughly investigated and
evaluated in Yang et al.’s work [46]. Among them, the
example-based methods [16], [25], [41], [47] achieve the
state-of-the-art performance.
The internal example-based methods exploit the self-
similarity property and generate exemplar patches from
the input image. It is ﬁrst proposed in Glasner’s
work [16], and several improved variants [13], [45] are
proposed to accelerate the implementation. The exter-
nal example-based methods [2], [4], [6], [15], [37], [41],
[48], [49], [50], [51] learn a mapping between low/high-
resolution patches from external datasets. These studies
vary on how to learn a compact dictionary or manifold
space to relate low/high-resolution patches, and on how
representation schemes can be conducted in such spaces.
In the pioneer work of Freeman et al. [14], the dic-
tionaries are directly presented as low/high-resolution
patch pairs, and the nearest neighbour (NN) of the input
patch is found in the low-resolution space, with its corre-
sponding high-resolution patch used for reconstruction.
Chang et al. [4] introduce a manifold embedding tech-
nique as an alternative to the NN strategy. In Yanget al.’s
work [49], [50], the above NN correspondence advances
to a more sophisticated sparse coding formulation. Other
mapping functions such as kernel regression [25], simple
3
function [47], random forest [37] and anchored neigh-
borhood regression [41], [42] are proposed to further
improve the mapping accuracy and speed. The sparse-
coding-based method and its several improvements [41],
[42], [48] are among the state-of-the-art SR methods
nowadays. In these methods, the patches are the focus
of the optimization; the patch extraction and aggregation
steps are considered as pre/post-processing and handled
separately.
The majority of SR algorithms [2], [4], [15], [41], [48],
[49], [50], [51] focus on gray-scale or single-channel
image super-resolution. For color images, the aforemen-
tioned methods ﬁrst transform the problem to a dif-
ferent color space (YCbCr or YUV), and SR is applied
only on the luminance channel. There are also works
attempting to super-resolve all channels simultaneously.
For example, Kim and Kwon [25] and Dai et al.[7] apply
their model to each RGB channel and combined them to
produce the ﬁnal results. However, none of them has
analyzed the SR performance of different channels, and
the necessity of recovering all three channels.
2.2 Convolutional Neural Networks
Convolutional neural networks (CNN) date back""",
            """1
Image Super-Resolution Using Deep
Convolutional Networks
Chao Dong, Chen Change Loy, Member, IEEE,Kaiming He, Member, IEEE,
and Xiaoou Tang, Fellow, IEEE
Abstract—We propose a deep learning method for single image super-resolution (SR). Our method directly learns an end-to-end
mapping between the low/high-resolution images. The mapping is represented as a deep convolutional neural network (CNN) that takes
the low-resolution image as the input and outputs the high-resolution one. We further show that traditional sparse-coding-based SR
methods can also be viewed as a deep convolutional network. But unlike traditional methods that handle each component separately,
our method jointly optimizes all layers. Our deep CNN has a lightweight structure, yet demonstrates state-of-the-art restoration quality,
and achieves fast speed for practical on-line usage. We explore different network structures and parameter settings to achieve trade-
offs between performance and speed. Moreover, we extend our network to cope with three color channels simultaneously, and show
better overall reconstruction quality.
Index Terms—Super-resolution, deep convolutional neural networks, sparse coding
!
1 I NTRODUCTION
Single image super-resolution (SR) [20], which aims at
recovering a high-resolution image from a single low-
resolution image, is a classical problem in computer
vision. This problem is inherently ill-posed since a mul-
tiplicity of solutions exist for any given low-resolution
pixel. In other words, it is an underdetermined in-
verse problem, of which solution is not unique. Such
a problem is typically mitigated by constraining the
solution space by strong prior information. To learn
the prior, recent state-of-the-art methods mostly adopt
the example-based [46] strategy. These methods either
exploit internal similarities of the same image [5], [13],
[16], [19], [47], or learn mapping functions from external
low- and high-resolution exemplar pairs [2], [4], [6],
[15], [23], [25], [37], [41], [42], [47], [48], [50], [51]. The
external example-based methods can be formulated for
generic image super-resolution, or can be designed to
suit domain speciﬁc tasks, i.e., face hallucination [30],
[50], according to the training samples provided.
The sparse-coding-based method [49], [50] is one of the
representative external example-based SR methods. This
method involves several steps in its solution pipeline.
First, overlapping patches are densely cropped from the
input image and pre-processed ( e.g.,subtracting mean
and normalization). These patches are then encoded
by a low-resolution dictionary. The sparse coefﬁcients
are passed into a high-resolution dictionary for recon-
structing high-resolution patches. The overlapping re-
• C. Dong, C. C. Loy and X. Tang are with the Department of Information
Engineering, The Chinese University of Hong Kong, Hong Kong.
E-mail: {dc012,ccloy,xtang}@ie.cuhk.edu.hk
• K. He is with the Visual Computing Group, Microsoft Research Asia,
Beijing 100080, China.
Email: kahe@microsoft.com
constructed patches are aggregated ( e.g., by weighted
averaging) to produce the ﬁnal output. This pipeline is
shared by most external example-based methods, which
pay particular attention to learning and optimizing the
dictionaries [2], [49], [50] or building efﬁcient mapping
functions [25], [41], [42], [47]. However, the rest of the
steps in the pipeline have been rarely optimized or
considered in an uniﬁed optimization framework.
In this paper, we show that the aforementioned
pipeline is equivalent to a deep convolutional neural net-
work [27] (more details in Section 3.2). Motivated by this
fact, we consider a convolutional neural network that
directly learns an end-to-end mapping between low- and
high-resolution images. Our method differs fundamen-
tally from existing external example-based approaches,
in that ours does not explicitly learn the dictionaries [41],
[49], [50] or manifolds [2], [4] for modeling the patch""",
            """bicubic interpolation. The training falls into a bad local
minimum, due to the inherently different characteristics
of the Y and Cb, Cr channels. (ii) If we pre-train on the
Y or Cb, Cr channels, the performance ﬁnally improves,
but is still not better than “Y only” on the color image
(see the last column of Table 5, where PSNR is computed
(a) First-layer ﬁlters – Cb channel
(b) First-layer ﬁlters – Cr channel
Fig. 13. Chrominance channels of the ﬁrst-layer ﬁlters
using the “Y pre-train” strategy.
in RGB color space). This suggests that the Cb, Cr
channels could decrease the performance of the Y chan-
nel when training is performed in a uniﬁed network.
(iii) We observe that the Cb, Cr channels have higher
PSNR values for “Y pre-train” than for “CbCr pre-train”.
The reason lies on the differences between the Cb, Cr
channels and the Y channel. Visually, the Cb, Cr channels
are more blurry than the Y channel, thus are less affected
by the downsampling process. When we pre-train on
the Cb, Cr channels, there are only a few ﬁlters being
activated. Then the training will soon fall into a bad
local minimum during ﬁne-tuning. On the other hand,
if we pre-train on the Y channel, more ﬁlters will be
activated, and the performance on Cb, Cr channels will
be pushed much higher. Figure 13 shows the Cb, Cr
channels of the ﬁrst-layer ﬁlters with “Y pre-train”, of
which the patterns largely differ from that shown in
Figure 5. (iv) Training on the RGB channels achieves
the best result on the color image. Different from the
YCbCr channels, the RGB channels exhibit high cross-
correlation among each other. The proposed SRCNN
is capable of leveraging such natural correspondences
between the channels for reconstruction. Therefore, the
model achieves comparable result on the Y channel as
“Y only”, and better results on Cb, Cr channels than
bicubic interpolation. (v) In KK [25], super-resolution
is applied on each RGB channel separately. When we
transform its results to YCbCr space, the PSNR value
of Y channel is similar as “Y only”, but that of Cb, Cr
channels are poorer than bicubic interpolation. The result
suggests that the algorithm is biased to the Y channel.
On the whole, our method trained on RGB channels
achieves better performance than KK and the single-
channel network (“Y only”). It is also worth noting that
the improvement compared with the single-channel net-
work is not that signiﬁcant ( i.e., 0.07 dB). This indicates
that the Cb, Cr channels barely help in improving the
performance.
5 C ONCLUSION
We have presented a novel deep learning approach
for single image super-resolution (SR). We show that
conventional sparse-coding-based SR methods can be
12
reformulated into a deep convolutional neural network.
The proposed approach, SRCNN, learns an end-to-end
mapping between low- and high-resolution images, with
little extra pre/post-processing beyond the optimization.
With a lightweight structure, the SRCNN has achieved
superior performance than the state-of-the-art methods.
We conjecture that additional performance can be further
gained by exploring more ﬁlters and different training
strategies. Besides, the proposed structure, with its ad-
vantages of simplicity and robustness, could be applied
to other low-level vision problems, such as image de-
blurring or simultaneous SR+denoising. One could also
investigate a network to cope with different upscaling
factors.
REFERENCES
[1] Aharon, M., Elad, M., Bruckstein, A.: K-SVD: An algorithm for
designing overcomplete dictionaries for sparse representation.
IEEE Transactions on Signal Processing 54(11), 4311–4322 (2006)
[2] Bevilacqua, M., Roumy, A., Guillemot, C., Morel, M.L.A.: Low-
complexity single-image super-resolution based on nonnegative
neighbor embedding. In: British Machine Vision Conference
(2012)
[3] Burger, H.C., Schuler, C.J., Harmeling, S.: Image denoising: Can
plain neural networks compete with BM3D? In: IEEE Conference""",
            """to generate the ﬁnal high-resolution image. This
image is expected to be similar to the ground truth
X.
We will show that all these operations form a convolu-
tional neural network. An overview of the network is
depicted in Figure 2. Next we detail our deﬁnition of
each operation.
3.1.1 Patch extraction and representation
A popular strategy in image restoration ( e.g., [1]) is to
densely extract patches and then represent them by a set
of pre-trained bases such as PCA, DCT, Haar, etc. This
is equivalent to convolving the image by a set of ﬁlters,
each of which is a basis. In our formulation, we involve
the optimization of these bases into the optimization of
the network. Formally, our ﬁrst layer is expressed as an
operation F1:
F1(Y) = max (0,W1 ∗Y + B1) , (1)
where W1 and B1 represent the ﬁlters and biases re-
spectively, and ’ ∗’ denotes the convolution operation.
Here, W1 corresponds to n1 ﬁlters of support c×f1 ×f1,
where c is the number of channels in the input image,
f1 is the spatial size of a ﬁlter. Intuitively, W1 applies
n1 convolutions on the image, and each convolution has
3. Bicubic interpolation is also a convolutional operation, so it can
be formulated as a convolutional layer. However, the output size of
this layer is larger than the input size, so there is a fractional stride. To
take advantage of the popular well-optimized implementations such
as cuda-convnet [26], we exclude this “layer” from learning.
4
feature maps
 Patch extraction
and representation Non-linear mapping Reconstruction
Low-resolution
image (input)
High-resolution
image (output)
of low-resolution image of high-resolution image
feature maps
Fig. 2. Given a low-resolution image Y, the ﬁrst convolutional layer of the SRCNN extracts a set of feature maps. The
second layer maps these feature maps nonlinearly to high-resolution patch representations. The last layer combines
the predictions within a spatial neighbourhood to produce the ﬁnal high-resolution image F(Y).
a kernel size c ×f1 ×f1. The output is composed of
n1 feature maps. B1 is an n1-dimensional vector, whose
each element is associated with a ﬁlter. We apply the
Rectiﬁed Linear Unit (ReLU, max(0,x)) [33] on the ﬁlter
responses4.
3.1.2 Non-linear mapping
The ﬁrst layer extracts an n1-dimensional feature for
each patch. In the second operation, we map each of
these n1-dimensional vectors into an n2-dimensional
one. This is equivalent to applying n2 ﬁlters which have
a trivial spatial support 1 ×1. This interpretation is only
valid for 1×1 ﬁlters. But it is easy to generalize to larger
ﬁlters like 3 ×3 or 5 ×5. In that case, the non-linear
mapping is not on a patch of the input image; instead,
it is on a 3 ×3 or 5 ×5 “patch” of the feature map. The
operation of the second layer is:
F2(Y) = max (0,W2 ∗F1(Y) + B2) . (2)
Here W2 contains n2 ﬁlters of size n1 ×f2 ×f2, and B2 is
n2-dimensional. Each of the output n2-dimensional vec-
tors is conceptually a representation of a high-resolution
patch that will be used for reconstruction.
It is possible to add more convolutional layers to
increase the non-linearity. But this can increase the com-
plexity of the model ( n2 ×f2 ×f2 ×n2 parameters for
one layer), and thus demands more training time. We
will explore deeper structures by introducing additional
non-linear mapping layers in Section 4.3.3.
3.1.3 Reconstruction
In the traditional methods, the predicted overlapping
high-resolution patches are often averaged to produce
the ﬁnal full image. The averaging can be considered
as a pre-deﬁned ﬁlter on a set of feature maps (where
each position is the “ﬂattened” vector form of a high-
resolution patch). Motivated by this, we deﬁne a convo-
lutional layer to produce the ﬁnal high-resolution image:
F(Y) = W3 ∗F2(Y) + B3. (3)
4. The ReLU can be equivalently considered as a part of the second
operation (Non-linear mapping), and the ﬁrst operation (Patch extrac-
tion and representation) becomes purely linear convolution.""",
            """erations, ηis the learning rate, and ∂L
∂W ℓ
i
is the derivative.
The ﬁlter weights of each layer are initialized by drawing
randomly from a Gaussian distribution with zero mean
and standard deviation 0.001 (and 0 for biases). The
learning rate is 10−4 for the ﬁrst two layers, and 10−5 for
the last layer. We empirically ﬁnd that a smaller learning
rate in the last layer is important for the network to
converge (similar to the denoising case [22]).
In the training phase, the ground truth images {Xi}
are prepared as fsub×fsub×c-pixel sub-images randomly
cropped from the training images. By “sub-images” we
mean these samples are treated as small “images” rather
than “patches”, in the sense that “patches” are overlap-
ping and require some averaging as post-processing but
“sub-images” need not. To synthesize the low-resolution
samples {Yi}, we blur a sub-image by a Gaussian kernel,
sub-sample it by the upscaling factor, and upscale it by
the same factor via bicubic interpolation.
To avoid border effects during training, all the con-
volutional layers have no padding, and the network
produces a smaller output ( (fsub −f1 −f2 −f3 + 3)2 ×c).
The MSE loss function is evaluated only by the difference
between the central pixels of Xi and the network output.
Although we use a ﬁxed image size in training, the
convolutional neural network can be applied on images
of arbitrary sizes during testing.
We implement our model using the cuda-convnet pack-
age [26]. We have also tried the Caffe package [24] and
observed similar performance.
4 E XPERIMENTS
We ﬁrst investigate the impact of using different datasets
on the model performance. Next, we examine the ﬁlters
learned by our approach. We then explore different
architecture designs of the network, and study the rela-
tions between super-resolution performance and factors
like depth, number of ﬁlters, and ﬁlter sizes. Subse-
quently, we compare our method with recent state-of-
the-arts both quantitatively and qualitatively. Following
[42], super-resolution is only applied on the luminance
channel (Y channel in YCbCr color space) in Sections 4.1-
4.4, so c = 1 in the ﬁrst/last layer, and performance
(e.g., PSNR and SSIM) is evaluated on the Y channel. At
last, we extend the network to cope with color images
and evaluate the performance on different channels.
4.1 Training Data
As shown in the literature, deep learning generally
beneﬁts from big data training. For comparison, we use
a relatively small training set [41], [50] that consists
of 91 images, and a large training set that consists of
395,909 images from the ILSVRC 2013 ImageNet detec-
tion training partition. The size of training sub-images is
fsub = 33. Thus the 91-image dataset can be decomposed
into 24,800 sub-images, which are extracted from origi-
nal images with a stride of 14. Whereas the ImageNet
provides over 5 million sub-images even using a stride
of 33. We use the basic network settings, i.e., f1 = 9 ,
f2 = 1, f3 = 5, n1 = 64, and n2 = 32. We use the Set5 [2]
as the validation set. We observe a similar trend even
if we use the larger Set14 set [51]. The upscaling factor
is 3. We use the sparse-coding-based method [50] as our
baseline, which achieves an average PSNR value of 31.42
dB.
The test convergence curves of using different training
sets are shown in Figure 4. The training time on Ima-
geNet is about the same as on the 91-image dataset since
the number of backpropagations is the same. As can be
observed, with the same number of backpropagations
(i.e.,8 ×108), the SRCNN +ImageNet achieves 32.52 dB,
higher than 32.39 dB yielded by that trained on 91
images. The results positively indicate that SRCNN per-
formance may be further boosted using a larger training
set, but the effect of big data is not as impressive as
that shown in high-level vision problems [26]. This is
mainly because that the 91 images have already cap-
tured sufﬁcient variability of natural images. On the""",
        ],
    ),
    LLMTestCase(
        input="Why do the authors of SRCNN first upscale the LR image with bicubic interpolation instead of learning that step end‑to‑end?",
        actual_output="""The authors of SRCNN pre-upscale the low-resolution (LR) image using bicubic interpolation (a standard image resizing technique) primarily to simplify the learning process and reduce computational cost. While learning the upscaling step end-to-end is possible, it would significantly increase the complexity of the model and require more resources for training. By pre-upscaling, the network only needs to learn the non-linear mapping between the interpolated image and the high-resolution image, which is a simpler task. They mention this is the only pre-processing step they perform.""",
        expected_output="""Because popular GPU conv‑net toolkits (cuda‑convnet at the time) did not yet support fractional‑stride convolutions. Upscaling once with bicubic ensures the network can stay fully convolutional with integer strides while still learning the rest of the SR mapping end‑to‑end.""",
        context=[
            """…we first upscale it to the desired size using bicubic interpolation, which is the only pre‑processing we perform. … There is a fractional stride. To take advantage of the popular well‑optimized implementations such as cuda‑convnet, we exclude this “layer” from learning."""
        ],
        retrieval_context=[
            """bicubic interpolation. The training falls into a bad local
minimum, due to the inherently different characteristics
of the Y and Cb, Cr channels. (ii) If we pre-train on the
Y or Cb, Cr channels, the performance ﬁnally improves,
but is still not better than “Y only” on the color image
(see the last column of Table 5, where PSNR is computed
(a) First-layer ﬁlters – Cb channel
(b) First-layer ﬁlters – Cr channel
Fig. 13. Chrominance channels of the ﬁrst-layer ﬁlters
using the “Y pre-train” strategy.
in RGB color space). This suggests that the Cb, Cr
channels could decrease the performance of the Y chan-
nel when training is performed in a uniﬁed network.
(iii) We observe that the Cb, Cr channels have higher
PSNR values for “Y pre-train” than for “CbCr pre-train”.
The reason lies on the differences between the Cb, Cr
channels and the Y channel. Visually, the Cb, Cr channels
are more blurry than the Y channel, thus are less affected
by the downsampling process. When we pre-train on
the Cb, Cr channels, there are only a few ﬁlters being
activated. Then the training will soon fall into a bad
local minimum during ﬁne-tuning. On the other hand,
if we pre-train on the Y channel, more ﬁlters will be
activated, and the performance on Cb, Cr channels will
be pushed much higher. Figure 13 shows the Cb, Cr
channels of the ﬁrst-layer ﬁlters with “Y pre-train”, of
which the patterns largely differ from that shown in
Figure 5. (iv) Training on the RGB channels achieves
the best result on the color image. Different from the
YCbCr channels, the RGB channels exhibit high cross-
correlation among each other. The proposed SRCNN
is capable of leveraging such natural correspondences
between the channels for reconstruction. Therefore, the
model achieves comparable result on the Y channel as
“Y only”, and better results on Cb, Cr channels than
bicubic interpolation. (v) In KK [25], super-resolution
is applied on each RGB channel separately. When we
transform its results to YCbCr space, the PSNR value
of Y channel is similar as “Y only”, but that of Cb, Cr
channels are poorer than bicubic interpolation. The result
suggests that the algorithm is biased to the Y channel.
On the whole, our method trained on RGB channels
achieves better performance than KK and the single-
channel network (“Y only”). It is also worth noting that
the improvement compared with the single-channel net-
work is not that signiﬁcant ( i.e., 0.07 dB). This indicates
that the Cb, Cr channels barely help in improving the
performance.
5 C ONCLUSION
We have presented a novel deep learning approach
for single image super-resolution (SR). We show that
conventional sparse-coding-based SR methods can be
12
reformulated into a deep convolutional neural network.
The proposed approach, SRCNN, learns an end-to-end
mapping between low- and high-resolution images, with
little extra pre/post-processing beyond the optimization.
With a lightweight structure, the SRCNN has achieved
superior performance than the state-of-the-art methods.
We conjecture that additional performance can be further
gained by exploring more ﬁlters and different training
strategies. Besides, the proposed structure, with its ad-
vantages of simplicity and robustness, could be applied
to other low-level vision problems, such as image de-
blurring or simultaneous SR+denoising. One could also
investigate a network to cope with different upscaling
factors.
REFERENCES
[1] Aharon, M., Elad, M., Bruckstein, A.: K-SVD: An algorithm for
designing overcomplete dictionaries for sparse representation.
IEEE Transactions on Signal Processing 54(11), 4311–4322 (2006)
[2] Bevilacqua, M., Roumy, A., Guillemot, C., Morel, M.L.A.: Low-
complexity single-image super-resolution based on nonnegative
neighbor embedding. In: British Machine Vision Conference
(2012)
[3] Burger, H.C., Schuler, C.J., Harmeling, S.: Image denoising: Can
plain neural networks compete with BM3D? In: IEEE Conference""",
            """In this paper, we show that the aforementioned
pipeline is equivalent to a deep convolutional neural net-
work [27] (more details in Section 3.2). Motivated by this
fact, we consider a convolutional neural network that
directly learns an end-to-end mapping between low- and
high-resolution images. Our method differs fundamen-
tally from existing external example-based approaches,
in that ours does not explicitly learn the dictionaries [41],
[49], [50] or manifolds [2], [4] for modeling the patch
space. These are implicitly achieved via hidden layers.
Furthermore, the patch extraction and aggregation are
also formulated as convolutional layers, so are involved
in the optimization. In our method, the entire SR pipeline
is fully obtained through learning, with little pre/post-
processing.
We name the proposed model Super-Resolution Con-
volutional Neural Network (SRCNN) 1. The proposed
SRCNN has several appealing properties. First, its struc-
ture is intentionally designed with simplicity in mind,
and yet provides superior accuracy 2 compared with
state-of-the-art example-based methods. Figure 1 shows
a comparison on an example. Second, with moderate
1. The implementation is available at http://mmlab.ie.cuhk.edu.hk/
projects/SRCNN.html.
2. Numerical evaluations by using different metrics such as the Peak
Signal-to-Noise Ratio (PSNR), structure similarity index (SSIM) [43],
multi-scale SSIM [44], information ﬁdelity criterion [38], when the
ground truth images are available.
arXiv:1501.00092v3  [cs.CV]  31 Jul 2015
2
Bicubic / 24.04 dB
SC / 25.58 dBSRCNN / 27.95 dB
Original / PSNR
2 4 6 8 10 12x 108
29.5
30
30.5
31
31.5
32
32.5
33
Number of backprops
Average test PSNR (dB)
SRCNN
SC
Bicubic
Bicubic / 24.04 dB
SC / 25.58 dBSRCNN / 27.95 dB
Original / PSNR
Bicubic / 24.04 dB
SC / 25.58 dBSRCNN / 27.95 dB
Original / PSNR
SRCNN
SC
Bicubic
Bicubic / 24.04 dB
SC / 25.58 dBSRCNN / 27.95 dB
Original / PSNR
Number of backprops
Average test PSNR (dB)
Fig. 1. The proposed Super-Resolution Convolutional
Neural Network (SRCNN) surpasses the bicubic baseline
with just a few training iterations, and outperforms the
sparse-coding-based method (SC) [50] with moderate
training. The performance may be further improved with
more training iterations. More details are provided in
Section 4.4.1 (the Set5 dataset with an upscaling factor
3). The proposed method provides visually appealing
reconstructed image.
numbers of ﬁlters and layers, our method achieves
fast speed for practical on-line usage even on a CPU.
Our method is faster than a number of example-based
methods, because it is fully feed-forward and does
not need to solve any optimization problem on usage.
Third, experiments show that the restoration quality of
the network can be further improved when (i) larger
and more diverse datasets are available, and/or (ii)
a larger and deeper model is used. On the contrary,
larger datasets/models can present challenges for exist-
ing example-based methods. Furthermore, the proposed
network can cope with three channels of color images
simultaneously to achieve improved super-resolution
performance.
Overall, the contributions of this study are mainly in
three aspects:
1) We present a fully convolutional neural net-
work for image super-resolution. The network di-
rectly learns an end-to-end mapping between low-
and high-resolution images, with little pre/post-
processing beyond the optimization.
2) We establish a relationship between our deep-
learning-based SR method and the traditional
sparse-coding-based SR methods. This relationship
provides a guidance for the design of the network
structure.
3) We demonstrate that deep learning is useful in
the classical computer vision problem of super-
resolution, and can achieve good quality and
speed.
A preliminary version of this work was presented
earlier [11]. The present work adds to the initial version
in signiﬁcant ways. Firstly, we improve the SRCNN by
introducing larger ﬁlter size in the non-linear mapping""",
            """terion (IFC) [38], noise quality measure (NQM) [8],
weighted peak signal-to-noise ratio (WPSNR) and multi-
scale structure similarity index (MSSSIM) [44], which
obtain high correlation with the human perceptual scores
as reported in [46].
4.4.1 Quantitative and qualitative evaluation
As shown in Tables 2, 3 and 4, the proposed SRCNN
yields the highest scores in most evaluation matrices
7. In the area of denoising [3], for each noise level a speciﬁc network
is trained.
8. We use the same 200 images as in [46].
9
2 4 6 8 10 12
x(10
8
30.5
31
31.5
32
32.5
33
Number(of(backprops
Average(test(PSNR((dB)
ANR - 31.92 dB
A+ - 32.59 dB
SRCNN
SC - 31.42 dB
Bicubic - 30.39 dB
NE+LLE - 31.84 dB
KK - 32.28 dB
Fig. 10. The test convergence curve of SRCNN and
results of other methods on the Set5 dataset.
in all experiments 9. Note that our SRCNN results are
based on the checkpoint of 8 ×108 backpropagations.
Speciﬁcally, for the upscaling factor 3, the average gains
on PSNR achieved by SRCNN are 0.15 dB, 0.17 dB, and
0.13 dB, higher than the next best approach, A+ [42],
on the three datasets. When we take a look at other
evaluation metrics, we observe that SC, to our surprise,
gets even lower scores than the bicubic interpolation
on IFC and NQM. It is clear that the results of SC are
more visually pleasing than that of bicubic interpolation.
This indicates that these two metrics may not truthfully
reveal the image quality. Thus, regardless of these two
metrics, SRCNN achieves the best performance among
all methods and scaling factors.
It is worth pointing out that SRCNN surpasses the
bicubic baseline at the very beginning of the learning
stage (see Figure 1), and with moderate training, SR-
CNN outperforms existing state-of-the-art methods (see
Figure 4). Yet, the performance is far from converge.
We conjecture that better results can be obtained given
longer training time (see Figure 10).
Figures 14, 15 and 16 show the super-resolution results
of different approaches by an upscaling factor 3. As can
be observed, the SRCNN produces much sharper edges
than other approaches without any obvious artifacts
across the image.
In addition, we report to another recent deep learning
method for image super-resolution (DNC) of Cui et
al. [5]. As they employ a different blur kernel (a Gaussian
ﬁlter with a standard deviation of 0.55), we train a spe-
ciﬁc network (9-5-5) using the same blur kernel as DNC
for fair quantitative comparison. The upscaling factor
is 3 and the training set is the 91-image dataset. From
the convergence curve shown in Figure 11, we observe
that our SRCNN surpasses DNC with just 2.7 ×107
backprops, and a larger margin can be obtained given
longer training time. This also demonstrates that the
end-to-end learning is superior to DNC, even if that
model is already “deep”.
4.4.2 Running time
Figure 12 shows the running time comparisons of several
state-of-the-art methods, along with their restoration
performance on Set14. All baseline methods are obtained
9. The PSNR value of each image can be found in the supplementary
ﬁle.
from the corresponding authors’ MATLAB+MEX imple-
mentation, whereas ours are in pure C++. We proﬁle
the running time of all the algorithms using the same
machine (Intel CPU 3.10 GHz and 16 GB memory).
Note that the processing time of our approach is highly
linear to the test image resolution, since all images go
through the same number of convolutions. Our method
is always a trade-off between performance and speed.
To show this, we train three networks for comparison,
which are 9-1-5, 9-3-5, and 9-5-5. It is clear that the 9-
1-5 network is the fastest, while it still achieves better
performance than the next state-of-the-art A+. Other
methods are several times or even orders of magnitude
slower in comparison to 9-1-5 network. Note the speed
gap is not mainly caused by the different MATLAB/C++
implementations; rather, the other methods need to solve
complex optimization problems on usage (e.g., sparse""",
            """4 0.7019 - 0.7331 0.7419 0.7352 0.7491 0.7513
2 6.09 - 7.59 6.83 7.81 8.11 7.76
IFC 3 3.41 2.98 4.14 3.83 4.23 4.45 4.26
4 2.23 - 2.71 2.57 2.78 2.94 2.74
2 40.98 - 41.34 38.86 41.79 42.61 38.95
NQM 3 33.15 29.06 37.12 35.23 37.22 38.24 35.25
4 26.15 - 31.17 29.18 31.27 32.31 30.46
2 47.64 - 54.47 53.85 54.57 55.62 55.39
WPSNR 3 39.72 41.66 43.22 43.56 43.36 44.25 44.32
4 35.71 - 37.75 38.26 37.85 38.72 38.87
2 0.9813 - 0.9886 0.9890 0.9888 0.9896 0.9897
MSSSIM 3 0.9512 0.9595 0.9643 0.9653 0.9647 0.9669 0.9675
4 0.9134 - 0.9317 0.9338 0.9326 0.9371 0.9376
TABLE 4
The average results of PSNR (dB), SSIM, IFC, NQM, WPSNR (dB) and MSSIM on the BSD200 dataset.
Eval. Mat Scale Bicubic SC [50] NE+LLE [4] KK [25] ANR [41] A+ [41] SRCNN
2 28.38 - 29.67 30.02 29.72 30.14 30.29
PSNR 3 25.94 26.54 26.67 26.89 26.72 27.05 27.18
4 24.65 - 25.21 25.38 25.25 25.51 25.60
2 0.8524 - 0.8886 0.8935 0.8900 0.8966 0.8977
SSIM 3 0.7469 0.7729 0.7823 0.7881 0.7843 0.7945 0.7971
4 0.6727 - 0.7037 0.7093 0.7060 0.7171 0.7184
2 5.30 - 7.10 6.33 7.28 7.51 7.21
IFC 3 3.05 2.77 3.82 3.52 3.91 4.07 3.91
4 1.95 - 2.45 2.24 2.51 2.62 2.45
2 36.84 - 41.52 38.54 41.72 42.37 39.66
NQM 3 28.45 28.22 34.65 33.45 34.81 35.58 34.72
4 21.72 - 25.15 24.87 25.27 26.01 25.65
2 46.15 - 52.56 52.21 52.69 53.56 53.58
WPSNR 3 38.60 40.48 41.39 41.62 41.53 42.19 42.29
4 34.86 - 36.52 36.80 36.64 37.18 37.24
2 0.9780 - 0.9869 0.9876 0.9872 0.9883 0.9883
MSSSIM 3 0.9426 0.9533 0.9575 0.9588 0.9581 0.9609 0.9614
4 0.9005 - 0.9203 0.9215 0.9214 0.9256 0.9261
11
10
0
10
1
10
228.2
28.4
28.6
28.8
29
29.2
29.4
Running time (sec)
PSNR (dB)
SC
NE+LLE ANR
KK
A+
SRCNN(9-1-5)
SRCNN(9-3-5) SRCNN(9-5-5)
——> FasterSlower <——
Fig. 12. The proposed SRCNN achieves the state-
of-the-art super-resolution quality, whilst maintains high
and competitive speed in comparison to existing external
example-based methods. The chart is based on Set14
results summarized in Table 3. The implementation of all
three SRCNN networks are available on our project page.
TABLE 5
Average PSNR (dB) of different channels and training
strategies on the Set5 dataset.
Training PSNR of different channel(s)
Strategies Y Cb Cr RGB color image
Bicubic 30.39 45.44 45.42 34.57
Y only 32.39 45.44 45.42 36.37
YCbCr 29.25 43.30 43.49 33.47
Y pre-train 32.19 46.49 46.45 36.32
CbCr pre-train 32.14 46.38 45.84 36.25
RGB 32.33 46.18 46.20 36.44
KK 32.37 44.35 44.22 36.32
effectiveness of SRCNN on different scales, here we only
evaluate the performance of upscaling factor 3.
Comparisons. We compare our method with the state-
of-art color SR method – KK [25]. We also try different
learning strategies for comparison:
• Y only: this is our baseline method, which is a
single-channel ( c = 1 ) network trained only on
the luminance channel. The Cb, Cr channels are
upscaled using bicubic interpolation.
• YCbCr: training is performed on the three channels
of the YCbCr space.
• Y pre-train: ﬁrst, to guarantee the performance on
the Y channel, we only use the MSE of the Y channel
as the loss to pre-train the network. Then we employ
the MSE of all channels to ﬁne-tune the parameters.
• CbCr pre-train: we use the MSE of the Cb, Cr
channels as the loss to pre-train the network, then
ﬁne-tune the parameters on all channels.
• RGB: training is performed on the three channels of
the RGB space.
The results are shown in Table 5, where we have the
following observations. (i) If we directly train on the
YCbCr channels, the results are even worse than that of
bicubic interpolation. The training falls into a bad local
minimum, due to the inherently different characteristics
of the Y and Cb, Cr channels. (ii) If we pre-train on the
Y or Cb, Cr channels, the performance ﬁnally improves,
but is still not better than “Y only” on the color image
(see the last column of Table 5, where PSNR is computed
(a) First-layer ﬁlters – Cb channel
(b) First-layer ﬁlters – Cr channel
Fig. 13. Chrominance channels of the ﬁrst-layer ﬁlters""",
            """erations, ηis the learning rate, and ∂L
∂W ℓ
i
is the derivative.
The ﬁlter weights of each layer are initialized by drawing
randomly from a Gaussian distribution with zero mean
and standard deviation 0.001 (and 0 for biases). The
learning rate is 10−4 for the ﬁrst two layers, and 10−5 for
the last layer. We empirically ﬁnd that a smaller learning
rate in the last layer is important for the network to
converge (similar to the denoising case [22]).
In the training phase, the ground truth images {Xi}
are prepared as fsub×fsub×c-pixel sub-images randomly
cropped from the training images. By “sub-images” we
mean these samples are treated as small “images” rather
than “patches”, in the sense that “patches” are overlap-
ping and require some averaging as post-processing but
“sub-images” need not. To synthesize the low-resolution
samples {Yi}, we blur a sub-image by a Gaussian kernel,
sub-sample it by the upscaling factor, and upscale it by
the same factor via bicubic interpolation.
To avoid border effects during training, all the con-
volutional layers have no padding, and the network
produces a smaller output ( (fsub −f1 −f2 −f3 + 3)2 ×c).
The MSE loss function is evaluated only by the difference
between the central pixels of Xi and the network output.
Although we use a ﬁxed image size in training, the
convolutional neural network can be applied on images
of arbitrary sizes during testing.
We implement our model using the cuda-convnet pack-
age [26]. We have also tried the Caffe package [24] and
observed similar performance.
4 E XPERIMENTS
We ﬁrst investigate the impact of using different datasets
on the model performance. Next, we examine the ﬁlters
learned by our approach. We then explore different
architecture designs of the network, and study the rela-
tions between super-resolution performance and factors
like depth, number of ﬁlters, and ﬁlter sizes. Subse-
quently, we compare our method with recent state-of-
the-arts both quantitatively and qualitatively. Following
[42], super-resolution is only applied on the luminance
channel (Y channel in YCbCr color space) in Sections 4.1-
4.4, so c = 1 in the ﬁrst/last layer, and performance
(e.g., PSNR and SSIM) is evaluated on the Y channel. At
last, we extend the network to cope with color images
and evaluate the performance on different channels.
4.1 Training Data
As shown in the literature, deep learning generally
beneﬁts from big data training. For comparison, we use
a relatively small training set [41], [50] that consists
of 91 images, and a large training set that consists of
395,909 images from the ILSVRC 2013 ImageNet detec-
tion training partition. The size of training sub-images is
fsub = 33. Thus the 91-image dataset can be decomposed
into 24,800 sub-images, which are extracted from origi-
nal images with a stride of 14. Whereas the ImageNet
provides over 5 million sub-images even using a stride
of 33. We use the basic network settings, i.e., f1 = 9 ,
f2 = 1, f3 = 5, n1 = 64, and n2 = 32. We use the Set5 [2]
as the validation set. We observe a similar trend even
if we use the larger Set14 set [51]. The upscaling factor
is 3. We use the sparse-coding-based method [50] as our
baseline, which achieves an average PSNR value of 31.42
dB.
The test convergence curves of using different training
sets are shown in Figure 4. The training time on Ima-
geNet is about the same as on the 91-image dataset since
the number of backpropagations is the same. As can be
observed, with the same number of backpropagations
(i.e.,8 ×108), the SRCNN +ImageNet achieves 32.52 dB,
higher than 32.39 dB yielded by that trained on 91
images. The results positively indicate that SRCNN per-
formance may be further boosted using a larger training
set, but the effect of big data is not as impressive as
that shown in high-level vision problems [26]. This is
mainly because that the 91 images have already cap-
tured sufﬁcient variability of natural images. On the""",
            """1 2 3 4 5 6 7 8
xR10
8
31.5
32
32.5
NumberRofRbackprops
AverageRtestRPSNRR(dB)
SRCNNR(9−5−5)
SRCNNR(9−5−1−5)
SCR(31.42RdB)
(c) 9-5-5 vs. 9-5-1-5
Fig. 8. Comparisons between three-layer and four-layer
networks.
mapping layers with n22 = 32 and n23 = 16 ﬁlters on
9-1-5, then we have to set a smaller learning rate to
ensure convergence, but we still do not observe superior
performance after a week of training (see Figure 9(a)).
We also tried to enlarge the ﬁlter size of the additional
layer to f22 = 3, and explore two deep structures – 9-3-
3-5 and 9-3-3-3. However, from the convergence curves
shown in Figure 9(b), these two networks do not show
better results than the 9-3-1-5 network.
All these experiments indicate that it is not “the deeper
the better” in this deep model for super-resolution. It
may be caused by the difﬁculty of training. Our CNN
network contains no pooling layer or full-connected
layer, thus it is sensitive to the initialization parameters
and learning rate. When we go deeper (e.g., 4 or 5 layers),
we ﬁnd it hard to set appropriate learning rates that
guarantee convergence. Even it converges, the network
may fall into a bad local minimum, and the learned
ﬁlters are of less diversity even given enough training
time. This phenomenon is also observed in [16], where
improper increase of depth leads to accuracy saturation
or degradation for image classiﬁcation. Why “deeper is
not better” is still an open question, which requires in-
vestigations to better understand gradients and training
dynamics in deep architectures. Therefore, we still adopt
three-layer networks in the following experiments.
4.4 Comparisons to State-of-the-Arts
In this section, we show the quantitative and qualitative
results of our method in comparison to state-of-the-art
2 4 6 8 10 12
x(10
8
31
31.5
32
32.5
Number(of(backprops
Average(test(PSNR(=dB)
SRCNN(=9−1−5)
SRCNN(=9−1−1−5,(n 22=16)
SRCNN(=9−1−1−5,(n 22=32)
SRCNN(=9−1−1−1−5,(n 22=32,(n 23=16)
SC(=31.42(dB)
(a) 9-1-1-5 ( n22 = 32) and 9-1-1-1-5 ( n22 = 32, n23 = 16)
1 2 3 4 5 6 7 8 9
xS10
8
31.5
32
32.5
NumberSofSbackprops
AverageStestSPSNRS(dB)
SRCNNS(9−3−5)
SRCNNS(9−3−1−5)
SRCNNS(9−3−3−5)
SRCNNS(9−3−3−3)
SCS(31.42SdB)
(b) 9-3-3-5 and 9-3-3-3
Fig. 9. Deeper structure does not always lead to better
results.
methods. We adopt the model with good performance-
speed trade-off: a three-layer network with f1 = 9, f2 =
5, f3 = 5, n1 = 64, and n2 = 32 trained on the ImageNet.
For each upscaling factor ∈{2,3,4}, we train a speciﬁc
network for that factor 7.
Comparisons. We compare our SRCNN with the state-
of-the-art SR methods:
• SC - sparse coding-based method of Yang et al. [50]
• NE+LLE - neighbour embedding + locally linear
embedding method [4]
• ANR - Anchored Neighbourhood Regression
method [41]
• A+ - Adjusted Anchored Neighbourhood Regres-
sion method [42], and
• KK - the method described in [25], which achieves
the best performance among external example-
based methods, according to the comprehensive
evaluation conducted in Yang et al.’s work [46]
The implementations are all from the publicly available
codes provided by the authors, and all images are down-
sampled using the same bicubic kernel.
Test set.The Set5 [2] (5 images), Set14 [51] (14 images)
and BSD200 [32] (200 images) 8 are used to evaluate the
performance of upscaling factors 2, 3, and 4.
Evaluation metrics. Apart from the widely used PSNR
and SSIM [43] indices, we also adopt another four
evaluation matrices, namely information ﬁdelity cri-
terion (IFC) [38], noise quality measure (NQM) [8],
weighted peak signal-to-noise ratio (WPSNR) and multi-
scale structure similarity index (MSSSIM) [44], which
obtain high correlation with the human perceptual scores
as reported in [46].
4.4.1 Quantitative and qualitative evaluation
As shown in Tables 2, 3 and 4, the proposed SRCNN
yields the highest scores in most evaluation matrices
7. In the area of denoising [3], for each noise level a speciﬁc network
is trained.""",
            """only on the luminance channel. There are also works
attempting to super-resolve all channels simultaneously.
For example, Kim and Kwon [25] and Dai et al.[7] apply
their model to each RGB channel and combined them to
produce the ﬁnal results. However, none of them has
analyzed the SR performance of different channels, and
the necessity of recovering all three channels.
2.2 Convolutional Neural Networks
Convolutional neural networks (CNN) date back
decades [27] and deep CNNs have recently shown an
explosive popularity partially due to its success in image
classiﬁcation [18], [26]. They have also been success-
fully applied to other computer vision ﬁelds, such as
object detection [34], [40], [52], face recognition [39], and
pedestrian detection [35]. Several factors are of central
importance in this progress: (i) the efﬁcient training
implementation on modern powerful GPUs [26], (ii) the
proposal of the Rectiﬁed Linear Unit (ReLU) [33] which
makes convergence much faster while still presents good
quality [26], and (iii) the easy access to an abundance of
data (like ImageNet [9]) for training larger models. Our
method also beneﬁts from these progresses.
2.3 Deep Learning for Image Restoration
There have been a few studies of using deep learning
techniques for image restoration. The multi-layer per-
ceptron (MLP), whose all layers are fully-connected (in
contrast to convolutional), is applied for natural image
denoising [3] and post-deblurring denoising [36]. More
closely related to our work, the convolutional neural net-
work is applied for natural image denoising [22] and re-
moving noisy patterns (dirt/rain) [12]. These restoration
problems are more or less denoising-driven. Cui et al.[5]
propose to embed auto-encoder networks in their super-
resolution pipeline under the notion internal example-
based approach [16]. The deep model is not speciﬁcally
designed to be an end-to-end solution, since each layer
of the cascade requires independent optimization of the
self-similarity search process and the auto-encoder. On
the contrary, the proposed SRCNN optimizes an end-to-
end mapping. Further, the SRCNN is faster at speed. It
is not only a quantitatively superior method, but also a
practically useful one.
3 C ONVOLUTIONAL NEURAL NETWORKS FOR
SUPER -RESOLUTION
3.1 Formulation
Consider a single low-resolution image, we ﬁrst upscale
it to the desired size using bicubic interpolation, which
is the only pre-processing we perform 3. Let us denote
the interpolated image as Y. Our goal is to recover
from Y an image F(Y) that is as similar as possible
to the ground truth high-resolution image X. For the
ease of presentation, we still call Y a “low-resolution”
image, although it has the same size as X. We wish to
learn a mapping F, which conceptually consists of three
operations:
1) Patch extraction and representation: this opera-
tion extracts (overlapping) patches from the low-
resolution image Y and represents each patch as a
high-dimensional vector. These vectors comprise a
set of feature maps, of which the number equals to
the dimensionality of the vectors.
2) Non-linear mapping: this operation nonlinearly
maps each high-dimensional vector onto another
high-dimensional vector. Each mapped vector is
conceptually the representation of a high-resolution
patch. These vectors comprise another set of feature
maps.
3) Reconstruction: this operation aggregates the
above high-resolution patch-wise representations
to generate the ﬁnal high-resolution image. This
image is expected to be similar to the ground truth
X.
We will show that all these operations form a convolu-
tional neural network. An overview of the network is
depicted in Figure 2. Next we detail our deﬁnition of
each operation.
3.1.1 Patch extraction and representation
A popular strategy in image restoration ( e.g., [1]) is to
densely extract patches and then represent them by a set
of pre-trained bases such as PCA, DCT, Haar, etc. This""",
            """sion [27], trees [46] or Random Forests [47]. In Dai et al.
[6] a multitude of patch-speciﬁc regressors is learned and
the most appropriate regressors selected during testing.
Recently convolutional neural network (CNN) based SR
algorithms have shown excellent performance. In Wang
et al. [59] the authors encode a sparse representation
prior into their feed-forward network architecture based on
the learned iterative shrinkage and thresholding algorithm
(LISTA) [23]. Dong et al. [9, 10] used bicubic interpolation
to upscale an input image and trained a three layer deep
fully convolutional network end-to-end to achieve state-
of-the-art SR performance. Subsequently, it was shown
that enabling the network to learn the upscaling ﬁlters
directly can further increase performance both in terms of
accuracy and speed [11, 48, 57]. With their deeply-recursive
convolutional network (DRCN), Kim et al. [34] presented
a highly performant architecture that allows for long-range
pixel dependencies while keeping the number of model
parameters small. Of particular relevance for our paper are
the works by Johnson et al. [33] and Bruna et al. [5],
who rely on a loss function closer to perceptual similarity
to recover visually more convincing HR images.
1.1.2 Design of convolutional neural networks
The state of the art for many computer vision problems is
meanwhile set by speciﬁcally designed CNN architectures
following the success of the work by Krizhevsky et al. [37].
It was shown that deeper network architectures can be
difﬁcult to train but have the potential to substantially
increase the network’s accuracy as they allow modeling
mappings of very high complexity [49, 51]. To efﬁ-
ciently train these deeper network architectures, batch-
normalization [32] is often used to counteract the internal
co-variate shift. Deeper network architectures have also
been shown to increase performance for SISR, e.g. Kim et
al. [34] formulate a recursive CNN and present state-of-the-
art results. Another powerful design choice that eases the
training of deep CNNs is the recently introduced concept of
residual blocks [29] and skip-connections [30, 34]. Skip-
connections relieve the network architecture of modeling
the identity mapping that is trivial in nature, however, po-
tentially non-trivial to represent with convolutional kernels.
In the context of SISR it was also shown that learning
upscaling ﬁlters is beneﬁcial in terms of accuracy and speed
[11, 48, 57]. This is an improvement over Dong et al. [10]
where bicubic interpolation is employed to upscale the LR
observation before feeding the image to the CNN.
1.1.3 Loss functions
Pixel-wise loss functions such as MSE struggle to handle
the uncertainty inherent in recovering lost high-frequency
details such as texture: minimizing MSE encourages ﬁnd-
ing pixel-wise averages of plausible solutions which are
typically overly-smooth and thus have poor perceptual qual-
ity [42, 33, 13, 5]. Reconstructions of varying perceptual
Figure 3: Illustration of patches from the natural image
manifold (red) and super-resolved patches obtained with
MSE (blue) and GAN (orange). The MSE-based solution
appears overly smooth due to the pixel-wise average of
possible solutions in the pixel space, while GAN drives the
reconstruction towards the natural image manifold produc-
ing perceptually more convincing solutions.
quality are exempliﬁed with corresponding PSNR in Fig-
ure 2. We illustrate the problem of minimizing MSE in Fig-
ure 3 where multiple potential solutions with high texture
details are averaged to create a smooth reconstruction.
In Mathieu et al. [42] and Denton et al. [7] the authors
tackled this problem by employing generative adversarial
networks (GANs) [22] for the application of image genera-
tion. Yu and Porikli [66] augment pixel-wise MSE loss with
a discriminator loss to train a network that super-resolves
face images with large upscaling factors ( 8×). GANs""",
        ],
    ),
    LLMTestCase(
        input="What exactly is meant by “perceptual loss” in SRGAN, and how is it computed from VGG feature maps?",
        actual_output="""Perceptual loss" in SRGAN (Super-Resolution Generative Adversarial Network) means that instead of simply comparing the generated super-resolved image and the original high-resolution image pixel by pixel, the network aims to make the super-resolved image perceptually similar – that is, look more like the original – to a human observer. This is different from traditional metrics like Mean Squared Error (MSE) which only measure pixel differences.

Here's how the perceptual loss is calculated using VGG (Visual Geometry Group network, a pre-trained Convolutional Neural Network used for image recognition) feature maps:

Both the super-resolved image (generated by the SRGAN) and the original high-resolution image are passed through a pre-trained VGG19 network.

The VGG19 network extracts feature maps from both images. Feature maps are representations of different visual features of the images at different levels of abstraction within the network.

The perceptual loss is calculated by comparing these feature maps from specific layers within the VGG19 network, typically the ReLU (Rectified Linear Unit, a type of activation function in neural networks) activation layers. The loss is based on the Euclidean distance (a measure of the straight-line distance between two points in a multi-dimensional space representing the feature maps) between the feature representations of the two images. A smaller distance implies greater perceptual similarity.

Specifically, SRGAN combines this VGG-based content loss with an adversarial loss from the discriminator network within the GAN framework. The discriminator is trained to distinguish between real high-resolution images and the super-resolved images. This adversarial loss helps to make the generated images look more realistic. The content loss ensures that the generated image captures the perceptual content of the original image. The combination of these two losses is the overall perceptual loss.""",
        expected_output="""It is a weighted sum of a content loss (Euclidean distance between VGG‑feature maps of SR vs. HR images) and an adversarial loss (−log D(G(I))). The VGG layers (e.g., φ5,4) provide semantics; the adversarial term pushes outputs onto the natural‑image manifold.""",
        context=[
            """We formulate the perceptual loss as the weighted sum of a content loss and an adversarial loss component … Content loss l_{VGG/i.j} = 1/(W_{i,j}H_{i,j}) Σ(φ_{i,j}(I_{HR}) − φ_{i,j}(G(I_{LR})))² … l_{Gen} = −log D(G(I_{LR}))"""
        ],
        retrieval_context=[
            """lSR is commonly modeled based on the MSE [10, 48], we
improve on Johnson et al. [33] and Bruna et al. [5] and
design a loss function that assesses a solution with respect
to perceptually relevant characteristics. We formulate the
perceptual loss as the weighted sum of a content loss ( lSR
X )
and an adversarial loss component as:
lSR = lSR
X
content loss
+ 10−3lSR
Gen  
adversarial loss  
perceptual loss (for VGG based content losses)
(3)
In the following we describe possible choices for the con-
tent loss lSR
X and the adversarial loss lSR
Gen.
2.2.1 Content loss
The pixel-wise MSE loss is calculated as:
lSR
MSE = 1
r2WH
rW∑
x=1
rH∑
y=1
(IHR
x,y −GθG(ILR)x,y)2 (4)
This is the most widely used optimization target for image
SR on which many state-of-the-art approaches rely [10,
48]. However, while achieving particularly high PSNR,
solutions of MSE optimization problems often lack high-
frequency content which results in perceptually unsatisfy-
ing solutions with overly smooth textures (c.f . Figure 2).
Instead of relying on pixel-wise losses we build on the
ideas of Gatys et al. [19], Bruna et al. [5] and Johnson et
al. [33] and use a loss function that is closer to perceptual
similarity. We deﬁne the VGG loss based on the ReLU
activation layers of the pre-trained 19 layer VGG network
described in Simonyan and Zisserman [49]. With φi,j we
indicate the feature map obtained by the j-th convolution
(after activation) before the i-th maxpooling layer within the
VGG19 network, which we consider given. We then deﬁne
the VGG loss as the euclidean distance between the feature
representations of a reconstructed image GθG(ILR) and the
reference image IHR:
lSR
VGG/i.j = 1
Wi,jHi,j
Wi,j∑
x=1
Hi,j∑
y=1
(φi,j(IHR)x,y
−φi,j(GθG(ILR))x,y)2
(5)
Here Wi,j and Hi,j describe the dimensions of the
respective feature maps within the VGG network.
2.2.2 Adversarial loss
In addition to the content losses described so far, we also
add the generative component of our GAN to the perceptual
loss. This encourages our network to favor solutions that
reside on the manifold of natural images, by trying to
fool the discriminator network. The generative loss lSR
Gen
is deﬁned based on the probabilities of the discriminator
DθD (GθG(ILR)) over all training samples as:
lSR
Gen =
N∑
n=1
−log DθD (GθG(ILR)) (6)
Here, DθD (GθG(ILR)) is the probability that the recon-
structed image GθG(ILR) is a natural HR image. For better
gradient behavior we minimize −log DθD (GθG(ILR)) in-
stead of log[1 −DθD (GθG(ILR))] [22].
3. Experiments
3.1. Data and similarity measures
We perform experiments on three widely used bench-
mark datasets Set5 [3], Set14 [69] and BSD100, the testing
set of BSD300 [41]. All experiments are performed with
a scale factor of 4× between low- and high-resolution
images. This corresponds to a 16×reduction in image
pixels. For fair comparison, all reported PSNR [dB] and
SSIM [58] measures were calculated on the y-channel of
center-cropped, removal of a 4-pixel wide strip from each
border, images using the daala package 1. Super-resolved
images for the reference methods, including nearest neigh-
bor, bicubic, SRCNN [9] and SelfExSR [31], were obtained
from online material supplementary to Huang et al. 2 [31]
and for DRCN from Kim et al. 3 [34]. Results obtained
with SRResNet (for losses: lSR
MSE and lSR
VGG/2.2) and the
SRGAN variants are available online4. Statistical tests were
performed as paired two-sided Wilcoxon signed-rank tests
and signiﬁcance determined at p< 0.05.
The reader may also be interested in an independently
developed GAN-based solution on GitHub 5. However it
only provides experimental results on a limited set of faces,
which is a more constrained and easier task.
3.2. Training details and parameters
We trained all networks on a NVIDIA Tesla M40 GPU
using a random sample of 350 thousand images from
the ImageNet database [45]. These images are distinct
from the testing images. We obtained the LR images""",
            """3.4. Investigation of content loss
We investigated the effect of different content loss
choices in the perceptual loss for the GAN-based networks.
Speciﬁcally we investigate lSR = lSR
X + 10−3lSR
Gen for the
following content losses lSR
X :
Table 1: Performance of different loss functions for SR-
ResNet and the adversarial networks on Set5 and Set14
benchmark data. MOS score signiﬁcantly higher (p< 0.05)
than with other losses in that category∗. [4×upscaling]
SRResNet- SRGAN-
Set5 MSE VGG22 MSE VGG22 VGG54
PSNR 32.05 30.51 30.64 29.84 29.40
SSIM 0.9019 0.8803 0.8701 0.8468 0.8472
MOS 3.37 3.46 3.77 3.78 3.58
Set14
PSNR 28.49 27.19 26.92 26.44 26.02
SSIM 0.8184 0.7807 0.7611 0.7518 0.7397
MOS 2.98 3.15 ∗ 3.43 3.57 3.72 ∗
•SRGAN-MSE: lSR
MSE, to investigate the adversarial
network with the standard MSE as content loss.
•SRGAN-VGG22: lSR
VGG/2.2 with φ2,2, a loss deﬁned
on feature maps representing lower-level features [68].
•SRGAN-VGG54: lSR
VGG/5.4 with φ5,4, a loss deﬁned
on feature maps of higher level features from deeper
network layers with more potential to focus on the
content of the images [68, 65, 40]. We refer to this
network as SRGAN in the following.
We also evaluate the performance of the generator network
without adversarial component for the two losses lSR
MSE
(SRResNet-MSE) and lSR
VGG/2.2 (SRResNet-VGG22). We
refer to SRResNet-MSE asSRResNet. Note, when training
SRResNet-VGG22 we added an additional total variation
loss with weight 2 ×10−8 to lSR
VGG/2.2 [2, 33]. Quantitative
results are summarized in Table 1 and visual examples
provided in Figure 6. Even combined with the adversarial
loss, MSE provides solutions with the highest PSNR values
that are, however, perceptually rather smooth and less
convincing than results achieved with a loss component
more sensitive to visual perception. This is caused by
competition between the MSE-based content loss and the
adversarial loss. We further attribute minor reconstruction
artifacts, which we observed in a minority of SRGAN-
MSE-based reconstructions, to those competing objectives.
We could not determine a signiﬁcantly best loss function
for SRResNet or SRGAN with respect to MOS score
on Set5. However, SRGAN-VGG54 signiﬁcantly outper-
formed other SRGAN and SRResNet variants on Set14 in
terms of MOS. We observed a trend that using the higher
level VGG feature maps φ5,4 yields better texture detail
when compared to φ2,2 (c.f . Figure 6). Further examples of
perceptual improvements through SRGAN over SRResNet
are provided in the supplementary material.
Figure 5: Color-coded distribution of MOS scores on
BSD100. For each method 2600 samples (100 images ×
26 raters) were assessed. Mean shown as red marker, where
the bins are centered around value i. [4×upscaling]
3.5. Performance of the ﬁnal networks
We compare the performance of SRResNet and SR-
GAN to NN, bicubic interpolation, and four state-of-the-
art methods. Quantitative results are summarized in Table
2 and conﬁrm that SRResNet (in terms of PSNR/SSIM)
sets a new state of the art on three benchmark datasets.
Please note that we used a publicly available framework
for evaluation (c.f . Section 3.1), reported values might thus
slightly deviate from those reported in the original papers.
We further obtained MOS ratings for SRGAN and all
reference methods on BSD100. Examples of images super-
resolved with SRResNet and SRGAN are depicted in the
supplementary material. The results shown in Table 2
conﬁrm that SRGAN outperforms all reference methods by
a large margin and sets a new state of the art for photo-
realistic image SR. All differences in MOS ( c.f . Table
2) are highly signiﬁcant on BSD100, except SRCNN vs.
SelfExSR. The distribution of all collected MOS ratings is
summarized in Figure 5.
4. Discussion and future work
We conﬁrmed the superior perceptual performance of
SRGAN using MOS testing. We have further shown that
standard quantitative measures such as PSNR and SSIM""",
            """obtained by applying a Gaussian ﬁlter toIHR followed by a
downsampling operation with downsampling factor r. For
an image with C color channels, we describe ILR by a
real-valued tensor of size W ×H ×C and IHR, ISR by
rW ×rH ×Crespectively.
Our ultimate goal is to train a generating function Gthat
estimates for a given LR input image its corresponding HR
counterpart. To achieve this, we train a generator network as
a feed-forward CNN GθG parametrized by θG. Here θG =
{W1:L; b1:L}denotes the weights and biases of a L-layer
deep network and is obtained by optimizing a SR-speciﬁc
loss function lSR. For training images IHR
n , n= 1,...,N
with corresponding ILR
n , n= 1,...,N , we solve:
ˆθG = arg min
θG
1
N
N∑
n=1
lSR(GθG(ILR
n ),IHR
n ) (1)
In this work we will speciﬁcally design a perceptual loss
lSR as a weighted combination of several loss components
that model distinct desirable characteristics of the recovered
SR image. The individual loss functions are described in
more detail in Section 2.2.
2.1. Adversarial network architecture
Following Goodfellow et al. [22] we further deﬁne
a discriminator network DθD which we optimize in an
alternating manner along with GθG to solve the adversarial
min-max problem:
min
θG
max
θD
EIHR∼ptrain(IHR)[log DθD (IHR)]+
EILR∼pG(ILR)[log(1 −DθD (GθG(ILR))]
(2)
The general idea behind this formulation is that it allows
one to train a generative model Gwith the goal of fooling a
differentiable discriminator Dthat is trained to distinguish
super-resolved images from real images. With this approach
our generator can learn to create solutions that are highly
similar to real images and thus difﬁcult to classify by D.
This encourages perceptually superior solutions residing in
the subspace, the manifold, of natural images. This is in
contrast to SR solutions obtained by minimizing pixel-wise
error measurements, such as the MSE.
At the core of our very deep generator networkG, which
is illustrated in Figure 4 areBresidual blocks with identical
layout. Inspired by Johnson et al. [33] we employ the block
layout proposed by Gross and Wilber [24]. Speciﬁcally, we
use two convolutional layers with small3×3 kernels and 64
feature maps followed by batch-normalization layers [32]
and ParametricReLU [28] as the activation function. We
increase the resolution of the input image with two trained
sub-pixel convolution layers as proposed by Shi et al. [48].
To discriminate real HR images from generated SR
samples we train a discriminator network. The architecture
is shown in Figure 4. We follow the architectural guidelines
summarized by Radford et al. [44] and use LeakyReLU
activation (α = 0.2) and avoid max-pooling throughout
the network. The discriminator network is trained to solve
the maximization problem in Equation 2. It contains eight
convolutional layers with an increasing number of 3 ×3
ﬁlter kernels, increasing by a factor of 2 from 64 to 512 ker-
nels as in the VGG network [49]. Strided convolutions are
used to reduce the image resolution each time the number
of features is doubled. The resulting 512 feature maps are
followed by two dense layers and a ﬁnal sigmoid activation
function to obtain a probability for sample classiﬁcation.
Figure 4: Architecture of Generator and Discriminator Network with corresponding kernel size (k), number of feature maps
(n) and stride (s) indicated for each convolutional layer.
2.2. Perceptual loss function
The deﬁnition of our perceptual loss function lSR is crit-
ical for the performance of our generator network. While
lSR is commonly modeled based on the MSE [10, 48], we
improve on Johnson et al. [33] and Bruna et al. [5] and
design a loss function that assesses a solution with respect
to perceptually relevant characteristics. We formulate the
perceptual loss as the weighted sum of a content loss ( lSR
X )
and an adversarial loss component as:
lSR = lSR
X
content loss
+ 10−3lSR
Gen  
adversarial loss  
perceptual loss (for VGG based content losses)
(3)""",
            """and signiﬁcance determined at p< 0.05.
The reader may also be interested in an independently
developed GAN-based solution on GitHub 5. However it
only provides experimental results on a limited set of faces,
which is a more constrained and easier task.
3.2. Training details and parameters
We trained all networks on a NVIDIA Tesla M40 GPU
using a random sample of 350 thousand images from
the ImageNet database [45]. These images are distinct
from the testing images. We obtained the LR images
by downsampling the HR images (BGR, C = 3) using
bicubic kernel with downsampling factor r = 4. For each
mini-batch we crop 16 random 96 ×96 HR sub images
of distinct training images. Note that we can apply the
generator model to images of arbitrary size as it is fully
1https://github.com/xiph/daala (commit: 8d03668)
2https://github.com/jbhuang0604/SelfExSR
3http://cv.snu.ac.kr/research/DRCN/
4https://twitter.box.com/s/
lcue6vlrd01ljkdtdkhmfvk7vtjhetog
5https://github.com/david-gpu/srez
convolutional. We scaled the range of the LR input images
to [0,1] and for the HR images to [−1,1]. The MSE loss
was thus calculated on images of intensity range [−1,1].
VGG feature maps were also rescaled by a factor of 1
12.75
to obtain VGG losses of a scale that is comparable to the
MSE loss. This is equivalent to multiplying Equation 5
with a rescaling factor of ≈ 0.006. For optimization we
use Adam [36] with β1 = 0.9. The SRResNet networks
were trained with a learning rate of 10−4 and 106 update
iterations. We employed the trained MSE-based SRResNet
network as initialization for the generator when training
the actual GAN to avoid undesired local optima. All
SRGAN variants were trained with 105 update iterations
at a learning rate of 10−4 and another 105 iterations at a
lower rate of 10−5. We alternate updates to the generator
and discriminator network, which is equivalent to k = 1
as used in Goodfellow et al. [22]. Our generator network
has 16 identical (B = 16) residual blocks. During test time
we turn batch-normalization update off to obtain an output
that deterministically depends only on the input [32]. Our
implementation is based on Theano [53] and Lasagne [8].
3.3. Mean opinion score (MOS) testing
We have performed a MOS test to quantify the ability of
different approaches to reconstruct perceptually convincing
images. Speciﬁcally, we asked 26 raters to assign an inte-
gral score from 1 (bad quality) to 5 (excellent quality) to the
super-resolved images. The raters rated 12 versions of each
image on Set5, Set14 and BSD100: nearest neighbor (NN),
bicubic, SRCNN [9], SelfExSR [31], DRCN [34], ESPCN
[48], SRResNet-MSE, SRResNet-VGG22∗ (∗not rated on
BSD100), SRGAN-MSE ∗, SRGAN-VGG22 ∗, SRGAN-
VGG54 and the original HR image. Each rater thus rated
1128 instances (12 versions of 19 images plus 9 versions of
100 images) that were presented in a randomized fashion.
The raters were calibrated on the NN (score 1) and HR (5)
versions of 20 images from the BSD300 training set. In a
pilot study we assessed the calibration procedure and the
test-retest reliability of 26 raters on a subset of 10 images
from BSD100 by adding a method’s images twice to a
larger test set. We found good reliability and no signiﬁcant
differences between the ratings of the identical images.
Raters very consistently rated NN interpolated test images
as 1 and the original HR images as 5 (c.f . Figure 5).
The experimental results of the conducted MOS tests are
summarized in Table 1, Table 2 and Figure 5.
3.4. Investigation of content loss
We investigated the effect of different content loss
choices in the perceptual loss for the GAN-based networks.
Speciﬁcally we investigate lSR = lSR
X + 10−3lSR
Gen for the
following content losses lSR
X :
Table 1: Performance of different loss functions for SR-
ResNet and the adversarial networks on Set5 and Set14
benchmark data. MOS score signiﬁcantly higher (p< 0.05)
than with other losses in that category∗. [4×upscaling]
SRResNet- SRGAN-""",
            """ure 3 where multiple potential solutions with high texture
details are averaged to create a smooth reconstruction.
In Mathieu et al. [42] and Denton et al. [7] the authors
tackled this problem by employing generative adversarial
networks (GANs) [22] for the application of image genera-
tion. Yu and Porikli [66] augment pixel-wise MSE loss with
a discriminator loss to train a network that super-resolves
face images with large upscaling factors ( 8×). GANs
were also used for unsupervised representation learning in
Radford et al. [44]. The idea of using GANs to learn a
mapping from one manifold to another is described by Li
and Wand [38] for style transfer and Yeh et al. [64] for
inpainting. Bruna et al. [5] minimize the squared error in
the feature spaces of VGG19 [49] and scattering networks.
Dosovitskiy and Brox [13] use loss functions based
on Euclidean distances computed in the feature space of
neural networks in combination with adversarial training.
It is shown that the proposed loss allows visually superior
image generation and can be used to solve the ill-posed
inverse problem of decoding nonlinear feature representa-
tions. Similar to this work, Johnson et al. [33] and Bruna
et al. [5] propose the use of features extracted from a pre-
trained VGG network instead of low-level pixel-wise error
measures. Speciﬁcally the authors formulate a loss function
based on the euclidean distance between feature maps
extracted from the VGG19 [49] network. Perceptually more
convincing results were obtained for both super-resolution
and artistic style-transfer [19, 20]. Recently, Li and Wand
[38] also investigated the effect of comparing and blending
patches in pixel or VGG feature space.
1.2. Contribution
GANs provide a powerful framework for generating
plausible-looking natural images with high perceptual qual-
ity. The GAN procedure encourages the reconstructions
to move towards regions of the search space with high
probability of containing photo-realistic images and thus
closer to the natural image manifold as shown in Figure 3.
In this paper we describe the ﬁrst very deep ResNet
[29, 30] architecture using the concept of GANs to form a
perceptual loss function for photo-realistic SISR. Our main
contributions are:
•We set a new state of the art for image SR with
high upscaling factors (4×) as measured by PSNR and
structural similarity (SSIM) with our 16 blocks deep
ResNet (SRResNet) optimized for MSE.
•We propose SRGAN which is a GAN-based network
optimized for a new perceptual loss. Here we replace
the MSE-based content loss with a loss calculated on
feature maps of the VGG network [49], which are
more invariant to changes in pixel space [38].
•We conﬁrm with an extensive mean opinion score
(MOS) test on images from three public benchmark
datasets that SRGAN is the new state of the art, by a
large margin, for the estimation of photo-realistic SR
images with high upscaling factors (4×).
We describe the network architecture and the perceptual
loss in Section 2. A quantitative evaluation on public bench-
mark datasets as well as visual illustrations are provided in
Section 3. The paper concludes with a discussion in Section
4 and concluding remarks in Section 5.
2. Method
In SISR the aim is to estimate a high-resolution, super-
resolved image ISR from a low-resolution input image
ILR. Here ILR is the low-resolution version of its high-
resolution counterpart IHR. The high-resolution images
are only available during training. In training, ILR is
obtained by applying a Gaussian ﬁlter toIHR followed by a
downsampling operation with downsampling factor r. For
an image with C color channels, we describe ILR by a
real-valued tensor of size W ×H ×C and IHR, ISR by
rW ×rH ×Crespectively.
Our ultimate goal is to train a generating function Gthat
estimates for a given LR input image its corresponding HR
counterpart. To achieve this, we train a generator network as
a feed-forward CNN GθG parametrized by θG. Here θG =""",
            """conﬁrm that SRGAN outperforms all reference methods by
a large margin and sets a new state of the art for photo-
realistic image SR. All differences in MOS ( c.f . Table
2) are highly signiﬁcant on BSD100, except SRCNN vs.
SelfExSR. The distribution of all collected MOS ratings is
summarized in Figure 5.
4. Discussion and future work
We conﬁrmed the superior perceptual performance of
SRGAN using MOS testing. We have further shown that
standard quantitative measures such as PSNR and SSIM
fail to capture and accurately assess image quality with
respect to the human visual system [56]. The focus of this
work was the perceptual quality of super-resolved images
rather than computational efﬁciency. The presented model
is, in contrast to Shi et al. [48], not optimized for video
SR in real-time. However, preliminary experiments on
the network architecture suggest that shallower networks
have the potential to provide very efﬁcient alternatives at
a small reduction of qualitative performance. In contrast to
Dong et al. [10], we found deeper network architectures to
be beneﬁcial. We speculate that the ResNet design has a
substantial impact on the performance of deeper networks.
We found that even deeper networks (B >16) can further
SRResNet SRGAN-MSE SRGAN-VGG22 SRGAN-VGG54 original HR image
Figure 6: SRResNet (left: a,b), SRGAN-MSE (middle left: c,d), SRGAN-VGG2.2 (middle: e,f) and SRGAN-VGG54
(middle right: g,h) reconstruction results and corresponding reference HR image (right: i,j). [ 4×upscaling]
Table 2: Comparison of NN, bicubic, SRCNN [9], SelfExSR [31], DRCN [34], ESPCN [48], SRResNet, SRGAN-VGG54
and the original HR on benchmark data. Highest measures (PSNR [dB], SSIM, MOS) in bold. [4×upscaling]
Set5 nearest bicubic SRCNN SelfExSR DRCN ESPCN SRResNet SRGAN HR
PSNR 26.26 28.43 30.07 30.33 31.52 30.76 32.05 29.40 ∞
SSIM 0.7552 0.8211 0.8627 0.872 0.8938 0.8784 0.9019 0.8472 1
MOS 1.28 1.97 2.57 2.65 3.26 2.89 3.37 3.58 4.32
Set14
PSNR 24.64 25.99 27.18 27.45 28.02 27.66 28.49 26.02 ∞
SSIM 0.7100 0.7486 0.7861 0.7972 0.8074 0.8004 0.8184 0.7397 1
MOS 1.20 1.80 2.26 2.34 2.84 2.52 2.98 3.72 4.32
BSD100
PSNR 25.02 25.94 26.68 26.83 27.21 27.02 27.58 25.16 ∞
SSIM 0.6606 0.6935 0.7291 0.7387 0.7493 0.7442 0.7620 0.6688 1
MOS 1.11 1.47 1.87 1.89 2.12 2.01 2.29 3.56 4.46
increase the performance of SRResNet, however, come at
the cost of longer training and testing times ( c.f . supple-
mentary material). We further found SRGAN variants of
deeper networks are increasingly difﬁcult to train due to the
appearance of high-frequency artifacts.
Of particular importance when aiming for photo-realistic
solutions to the SR problem is the choice of the content loss
as illustrated in Figure 6. In this work, we found lSR
VGG/5.4
to yield the perceptually most convincing results, which
we attribute to the potential of deeper network layers to
represent features of higher abstraction [68, 65, 40] away
from pixel space. We speculate that feature maps of these
deeper layers focus purely on the content while leaving the
adversarial loss focusing on texture details which are the
main difference between the super-resolved images without
the adversarial loss and photo-realistic images. We also
note that the ideal loss function depends on the application.
For example, approaches that hallucinate ﬁner detail might
be less suited for medical applications or surveillance. The
perceptually convincing reconstruction of text or structured
scenes [31] is challenging and part of future work. The
development of content loss functions that describe image
spatial content, but more invariant to changes in pixel space
will further improve photo-realistic image SR results.
5. Conclusion
We have described a deep residual network SRRes-
Net that sets a new state of the art on public benchmark
datasets when evaluated with the widely used PSNR mea-
sure. We have highlighted some limitations of this PSNR-
focused image super-resolution and introduced SRGAN,""",
            """Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial
Network
Christian Ledig, Lucas Theis, Ferenc Husz´ar, Jose Caballero, Andrew Cunningham,
Alejandro Acosta, Andrew Aitken, Alykhan Tejani, Johannes Totz, Zehan Wang, Wenzhe Shi
Twitter
{cledig,ltheis,fhuszar,jcaballero,aacostadiaz,aaitken,atejani,jtotz,zehanw,wshi}@twitter.com
Abstract
Despite the breakthroughs in accuracy and speed of
single image super-resolution using faster and deeper con-
volutional neural networks, one central problem remains
largely unsolved: how do we recover the ﬁner texture details
when we super-resolve at large upscaling factors? The
behavior of optimization-based super-resolution methods is
principally driven by the choice of the objective function.
Recent work has largely focused on minimizing the mean
squared reconstruction error. The resulting estimates have
high peak signal-to-noise ratios, but they are often lacking
high-frequency details and are perceptually unsatisfying in
the sense that they fail to match the ﬁdelity expected at
the higher resolution. In this paper, we present SRGAN,
a generative adversarial network (GAN) for image super-
resolution (SR). To our knowledge, it is the ﬁrst framework
capable of inferring photo-realistic natural images for 4×
upscaling factors. To achieve this, we propose a perceptual
loss function which consists of an adversarial loss and a
content loss. The adversarial loss pushes our solution to
the natural image manifold using a discriminator network
that is trained to differentiate between the super-resolved
images and original photo-realistic images. In addition, we
use a content loss motivated by perceptual similarity instead
of similarity in pixel space. Our deep residual network
is able to recover photo-realistic textures from heavily
downsampled images on public benchmarks. An extensive
mean-opinion-score (MOS) test shows hugely signiﬁcant
gains in perceptual quality using SRGAN. The MOS scores
obtained with SRGAN are closer to those of the original
high-resolution images than to those obtained with any
state-of-the-art method.
1. Introduction
The highly challenging task of estimating a high-
resolution (HR) image from its low-resolution (LR)
counterpart is referred to as super-resolution (SR). SR
received substantial attention from within the computer
vision research community and has a wide range of
applications [63, 71, 43].
4×SRGAN (proposed) original
Figure 1: Super-resolved image (left) is almost indistin-
guishable from original (right). [4×upscaling]
The ill-posed nature of the underdetermined SR problem
is particularly pronounced for high upscaling factors, for
which texture detail in the reconstructed SR images is
typically absent. The optimization target of supervised
SR algorithms is commonly the minimization of the mean
squared error (MSE) between the recovered HR image
and the ground truth. This is convenient as minimizing
MSE also maximizes the peak signal-to-noise ratio (PSNR),
which is a common measure used to evaluate and compare
SR algorithms [61]. However, the ability of MSE (and
PSNR) to capture perceptually relevant differences, such
as high texture detail, is very limited as they are deﬁned
based on pixel-wise image differences [60, 58, 26]. This
is illustrated in Figure 2, where highest PSNR does not
necessarily reﬂect the perceptually better SR result. The
1
arXiv:1609.04802v5  [cs.CV]  25 May 2017
bicubic SRResNet SRGAN original
(21.59dB/0.6423) (23.53dB/0.7832) (21.15dB/0.6868)
Figure 2: From left to right: bicubic interpolation, deep residual network optimized for MSE, deep residual generative
adversarial network optimized for a loss more sensitive to human perception, original HR image. Corresponding PSNR and
SSIM are shown in brackets. [4×upscaling]
perceptual difference between the super-resolved and orig-
inal image means that the recovered image is not photo-
realistic as deﬁned by Ferwerda [16].""",
            """[70] K. Zhang, X. Gao, D. Tao, and X. Li. Multi-scale dictionary for
single image super-resolution. In IEEE Conference on Computer
Vision and Pattern Recognition (CVPR), pages 1114–1121, 2012. 2
[71] W. Zou and P. C. Yuen. Very Low Resolution Face Recognition
in Parallel Environment . IEEE Transactions on Image Processing,
21:327–340, 2012. 1
A. Supplementary Material
In this supplementary material we ﬁrst brieﬂy investigate the inﬂuence of network depth (number of residual blocks)
on the performance (PSNR, time) of SRResNet in Section A.1. We then visualize on an example image how the SRGAN
network performance evolves with increasing number of training iterations in Section A.2. Results of the MOS tests
conducted on Set5, Set14, BSD100 are summarized in Section A.3. Finally we provide a visualization of all image
reconstruction obtained with SRResNet and SRGAN with a 4×upscaling factor for Set5 (Section A.4), Set14 (Section A.5)
and ﬁve randomly selected images from BSD100 (Section A.6).
Images are best viewed and compared zoomed in. All original low-/high-resolution images and reconstructions
(4×upscaling) obtained with different methods (bicubic, SRResNet-MSE, SRResNet-VGG22, SRGAN-MSE, SRGAN-
VGG22, SRGAN-VGG54) described in the paper are available for download at https://twitter.box.com/s/
lcue6vlrd01ljkdtdkhmfvk7vtjhetog.
A.1. Performance (PSNR/time) vs. network depth
We investigated the inﬂuence of network depth, speciﬁcally the number of residual blocks, on performance (PSNR [dB]
on BSD100 for 4×SR) and inference time [s] of the network architecture described in Figure 4 of the main paper. Time was
assessed on a NVIDIA M40 GPU and averaged over 100 reconstructions of a random low-resolution image with resolution
64×64 with upscaling factor 4×. The measurements are plotted in Figure 7 for a network with (blue) and without (red)
skip-connection. As expected the time of a single forward pass through the network depends approximately linearly on the
number of residual blocks. Whether a skip-connection is used or not has no substantial impact on inference time. However,
we observed substantial gains in performance with the additional skip-connection. We chose a network architecture of
16 residual blocks with skip-connection for the evaluation presented in the main paper as we consider this as good trade-
off between accuracy and speed including training time. While accuracy gains slowly saturate beyond 16 blocks there is,
nevertheless, a clear beneﬁt of using even deeper networks.
Figure 7: Dependence of network performance (PSNR, time) on network depth. PSNR (left) calculated on BSD100. Time
(right) averaged over 100 reconstructions of a random LR image with resolution 64×64.
A.2. Evolution of Generator during SRGAN training
We further investigated how reconstructions of the SRGAN generator network evolve (visually) with increasing number
of training iterations. Visual results obtained after different number of training iterations are illustrated in Figure 8. It is
interesting that after only 20 thousand training iterations the generator substantially diverged from the SRResNet initialization
and produces reconstruction with a lot of high frequency content, including noise. With increasing number of training
iterations reconstructions of the baboon from Set14 appear closer to the reference image. However, there is visually little
change during the last 50-100 thousand update iterations.
SRResNet 20k 40k 60k 80k
100k 140k 180k SRGAN original HR image
Figure 8: Evolution of SRGAN generator network during training progress. Note: Generator initialized with SRResNet
weights; learning rate set to 10−4 for ﬁrst 100k iterations, then reduced to 10−5 for another 100k iterations. [4×upscaling]
A.3. Mean opinion score (MOS) testing
In all conducted MOS tests we have asked 26 human raters to assign a score from 1 (Bad) to 5 (Excellent) to reconstructions""",
        ],
    ),
    LLMTestCase(
        input="SRCNN reports 8 032 trainable parameters; can you explain how this relatively small count is achieved?",
        actual_output="""SRCNN's relatively low parameter count of 8,032 is a result of its simple three-layer architecture and relatively small filter sizes. Let's break down how the parameter count is calculated:

Layer 1 (Patch extraction and representation): This layer uses 64 filters (kernels) with a size of 9x9x1. Since the input is assumed to be a single-channel image (grayscale), each filter has 9*9 = 81 weights, plus one bias term per filter. This results in 64 * (81 + 1) = 5,184 parameters for the first layer.

Layer 2 (Non-linear mapping): This layer employs 32 filters with a size of 1x1x64. The input to this layer is the output from the first layer, which has 64 channels. So each filter has 1164 = 64 weights, plus one bias term. This leads to 32 * (64 + 1) = 2,080 parameters in the second layer.

Layer 3 (Reconstruction): The final layer has a single filter with a size of 5x5x32. It takes the 32-channel output of the second layer as input. The filter has 5532 = 800 weights, plus a single bias term. This totals 800 + 1 = 801 parameters for the third layer.

Adding the parameters from all three layers: 5,184 + 2,080 + 801 = 8,065. The original paper mentions 8,032, suggesting a slight variation in the calculation. While the exact reason for this minor difference is unclear within the provided text, the primary reason for the low number of parameters is the smaller filter sizes compared to many deeper convolutional neural networks (CNNs), which might have hundreds or thousands of filters and larger filter dimensions, leading to millions or even billions of parameters.""",
        expected_output="""Because it uses just three convolutional layers with relatively few filters (64, 32, c) and small kernels (9×9, 1×1, 5×5). Param count = (c·9²·64)+(64·1²·32)+(32·5²·c)+biases ≈ 8 k""",
        context=[
            """A typical and basic setting is f₁ = 9, f₂ = 1, f₃ = 5, n₁ = 64, n₂ = 32 … the number of parameters of 9‑1‑5 … is 8 032."""
        ],
        retrieval_context=[
            """observed, with the same number of backpropagations
(i.e.,8 ×108), the SRCNN +ImageNet achieves 32.52 dB,
higher than 32.39 dB yielded by that trained on 91
images. The results positively indicate that SRCNN per-
formance may be further boosted using a larger training
set, but the effect of big data is not as impressive as
that shown in high-level vision problems [26]. This is
mainly because that the 91 images have already cap-
tured sufﬁcient variability of natural images. On the
other hand, our SRCNN is a relatively small network
(8,032 parameters), which could not overﬁt the 91 images
(24,800 samples). Nevertheless, we adopt the ImageNet,
which contains more diverse data, as the default training
set in the following experiments.
4.2 Learned Filters for Super-Resolution
Figure 5 shows examples of learned ﬁrst-layer ﬁlters
trained on the ImageNet by an upscaling factor 3. Please
refer to our published implementation for upscaling
factors 2 and 4. Interestingly, each learned ﬁlter has
its speciﬁc functionality. For instance, the ﬁlters g and
h are like Laplacian/Gaussian ﬁlters, the ﬁlters a - e
are like edge detectors at different directions, and the
ﬁlter f is like a texture extractor. Example feature maps
of different layers are shown in ﬁgure 6. Obviously,
feature maps of the ﬁrst layer contain different structures
(e.g., edges at different directions), while that of the
second layer are mainly different on intensities.
4.3 Model and Performance Trade-offs
Based on the basic network settings ( i.e., f1 = 9, f2 = 1,
f3 = 5 , n1 = 64 , and n2 = 32 ), we will progressively
modify some of these parameters to investigate the best
trade-off between performance and speed, and study the
relations between performance and parameters.
1 2 3 4 5 6 7 8 9 10
xS10
8
31.4
31.6
31.8
32
32.2
32.4
32.6
NumberSofSbackprops
AverageStestSPSNRSndBI
SRCNNSntrainedSonSImageNetI
SRCNNSntrainedSonS91SimagesI
SCSn31.42SdBI
Fig. 4. Training with the much larger ImageNet dataset
improves the performance over the use of 91 images.
7
a b c d e f
g
h
Fig. 5. The ﬁgure shows the ﬁrst-layer ﬁlters trained
on ImageNet with an upscaling factor 3. The ﬁlters are
organized based on their respective variances.
Input Feature maps of the first layer
Output Feature maps of the second layer
Fig. 6. Example feature maps of different layers.
4.3.1 Filter number
In general, the performance would improve if we in-
crease the network width6, i.e., adding more ﬁlters, at the
cost of running time. Speciﬁcally, based on our network
default settings of n1 = 64 and n2 = 32 , we conduct
two experiments: (i) one is with a larger network with
n1 = 128 and n2 = 64, and (ii) the other is with a smaller
network with n1 = 32 and n2 = 16. Similar to Section 4.1,
we also train the two models on ImageNet and test on
Set5 with an upscaling factor 3. The results observed
at 8 ×108 backpropagations are shown in Table 1. It is
clear that superior performance could be achieved by
increasing the width. However, if a fast restoration speed
is desired, a small network width is preferred, which
could still achieve better performance than the sparse-
coding-based method (31.42 dB).
TABLE 1
The results of using different ﬁlter numbers in SRCNN.
Training is performed on ImageNet whilst the evaluation
is conducted on the Set5 dataset.
n1 = 128 n1 = 64 n1 = 32
n2 = 64 n2 = 32 n2 = 16
PSNR Time (sec) PSNR Time (sec) PSNR Time (sec)
32.60 0.60 32.52 0.18 32.26 0.05
4.3.2 Filter size
In this section, we examine the network sensitivity to
different ﬁlter sizes. In previous experiments, we set
ﬁlter size f1 = 9, f2 = 1 and f3 = 5, and the network
could be denoted as 9-1-5. First, to be consistent with
sparse-coding-based methods, we ﬁx the ﬁlter size of the
second layer to be f2 = 1, and enlarge the ﬁlter size of
other layers to f1 = 11 and f3 = 7 (11-1-7). All the other
6. We use ‘width’ to term the number of ﬁlters in a layer, follow-""",
            """erations, ηis the learning rate, and ∂L
∂W ℓ
i
is the derivative.
The ﬁlter weights of each layer are initialized by drawing
randomly from a Gaussian distribution with zero mean
and standard deviation 0.001 (and 0 for biases). The
learning rate is 10−4 for the ﬁrst two layers, and 10−5 for
the last layer. We empirically ﬁnd that a smaller learning
rate in the last layer is important for the network to
converge (similar to the denoising case [22]).
In the training phase, the ground truth images {Xi}
are prepared as fsub×fsub×c-pixel sub-images randomly
cropped from the training images. By “sub-images” we
mean these samples are treated as small “images” rather
than “patches”, in the sense that “patches” are overlap-
ping and require some averaging as post-processing but
“sub-images” need not. To synthesize the low-resolution
samples {Yi}, we blur a sub-image by a Gaussian kernel,
sub-sample it by the upscaling factor, and upscale it by
the same factor via bicubic interpolation.
To avoid border effects during training, all the con-
volutional layers have no padding, and the network
produces a smaller output ( (fsub −f1 −f2 −f3 + 3)2 ×c).
The MSE loss function is evaluated only by the difference
between the central pixels of Xi and the network output.
Although we use a ﬁxed image size in training, the
convolutional neural network can be applied on images
of arbitrary sizes during testing.
We implement our model using the cuda-convnet pack-
age [26]. We have also tried the Caffe package [24] and
observed similar performance.
4 E XPERIMENTS
We ﬁrst investigate the impact of using different datasets
on the model performance. Next, we examine the ﬁlters
learned by our approach. We then explore different
architecture designs of the network, and study the rela-
tions between super-resolution performance and factors
like depth, number of ﬁlters, and ﬁlter sizes. Subse-
quently, we compare our method with recent state-of-
the-arts both quantitatively and qualitatively. Following
[42], super-resolution is only applied on the luminance
channel (Y channel in YCbCr color space) in Sections 4.1-
4.4, so c = 1 in the ﬁrst/last layer, and performance
(e.g., PSNR and SSIM) is evaluated on the Y channel. At
last, we extend the network to cope with color images
and evaluate the performance on different channels.
4.1 Training Data
As shown in the literature, deep learning generally
beneﬁts from big data training. For comparison, we use
a relatively small training set [41], [50] that consists
of 91 images, and a large training set that consists of
395,909 images from the ILSVRC 2013 ImageNet detec-
tion training partition. The size of training sub-images is
fsub = 33. Thus the 91-image dataset can be decomposed
into 24,800 sub-images, which are extracted from origi-
nal images with a stride of 14. Whereas the ImageNet
provides over 5 million sub-images even using a stride
of 33. We use the basic network settings, i.e., f1 = 9 ,
f2 = 1, f3 = 5, n1 = 64, and n2 = 32. We use the Set5 [2]
as the validation set. We observe a similar trend even
if we use the larger Set14 set [51]. The upscaling factor
is 3. We use the sparse-coding-based method [50] as our
baseline, which achieves an average PSNR value of 31.42
dB.
The test convergence curves of using different training
sets are shown in Figure 4. The training time on Ima-
geNet is about the same as on the 91-image dataset since
the number of backpropagations is the same. As can be
observed, with the same number of backpropagations
(i.e.,8 ×108), the SRCNN +ImageNet achieves 32.52 dB,
higher than 32.39 dB yielded by that trained on 91
images. The results positively indicate that SRCNN per-
formance may be further boosted using a larger training
set, but the effect of big data is not as impressive as
that shown in high-level vision problems [26]. This is
mainly because that the 91 images have already cap-
tured sufﬁcient variability of natural images. On the""",
            """the ﬁnal full image. The averaging can be considered
as a pre-deﬁned ﬁlter on a set of feature maps (where
each position is the “ﬂattened” vector form of a high-
resolution patch). Motivated by this, we deﬁne a convo-
lutional layer to produce the ﬁnal high-resolution image:
F(Y) = W3 ∗F2(Y) + B3. (3)
4. The ReLU can be equivalently considered as a part of the second
operation (Non-linear mapping), and the ﬁrst operation (Patch extrac-
tion and representation) becomes purely linear convolution.
Here W3 corresponds to c ﬁlters of a size n2 ×f3 ×f3,
and B3 is a c-dimensional vector.
If the representations of the high-resolution patches
are in the image domain (i.e.,we can simply reshape each
representation to form the patch), we expect that the
ﬁlters act like an averaging ﬁlter; if the representations
of the high-resolution patches are in some other domains
(e.g.,coefﬁcients in terms of some bases), we expect that
W3 behaves like ﬁrst projecting the coefﬁcients onto the
image domain and then averaging. In either way, W3 is
a set of linear ﬁlters.
Interestingly, although the above three operations are
motivated by different intuitions, they all lead to the
same form as a convolutional layer. We put all three
operations together and form a convolutional neural
network (Figure 2). In this model, all the ﬁltering weights
and biases are to be optimized. Despite the succinctness
of the overall structure, our SRCNN model is carefully
developed by drawing extensive experience resulted
from signiﬁcant progresses in super-resolution [49], [50].
We detail the relationship in the next section.
3.2 Relationship to Sparse-Coding-Based Methods
We show that the sparse-coding-based SR methods [49],
[50] can be viewed as a convolutional neural network.
Figure 3 shows an illustration.
In the sparse-coding-based methods, let us consider
that an f1 ×f1 low-resolution patch is extracted from
the input image. Then the sparse coding solver, like
Feature-Sign [29], will ﬁrst project the patch onto a (low-
resolution) dictionary. If the dictionary size is n1, this
is equivalent to applying n1 linear ﬁlters ( f1 ×f1) on
the input image (the mean subtraction is also a linear
operation so can be absorbed). This is illustrated as the
left part of Figure 3.
The sparse coding solver will then iteratively process
the n1 coefﬁcients. The outputs of this solver are n2
coefﬁcients, and usually n2 = n1 in the case of sparse
coding. These n2 coefﬁcients are the representation of
the high-resolution patch. In this sense, the sparse coding
5
responses
of patch of
neighbouring
patches
 Patch extraction
and representation
Non-linear
 mapping
Reconstruction
Fig. 3. An illustration of sparse-coding-based methods in the view of a convolutional neural network.
solver behaves as a special case of a non-linear mapping
operator, whose spatial support is 1 ×1. See the middle
part of Figure 3. However, the sparse coding solver is
not feed-forward, i.e.,it is an iterative algorithm. On the
contrary, our non-linear operator is fully feed-forward
and can be computed efﬁciently. If we set f2 = 1, then
our non-linear operator can be considered as a pixel-wise
fully-connected layer. It is worth noting that “the sparse
coding solver” in SRCNN refers to the ﬁrst two layers,
but not just the second layer or the activation function
(ReLU). Thus the nonlinear operation in SRCNN is also
well optimized through the learning process.
The above n2 coefﬁcients (after sparse coding) are
then projected onto another (high-resolution) dictionary
to produce a high-resolution patch. The overlapping
high-resolution patches are then averaged. As discussed
above, this is equivalent to linear convolutions on the
n2 feature maps. If the high-resolution patches used for
reconstruction are of size f3 ×f3, then the linear ﬁlters
have an equivalent spatial support of size f3 ×f3. See
the right part of Figure 3.
The above discussion shows that the sparse-coding-""",
            """then projected onto another (high-resolution) dictionary
to produce a high-resolution patch. The overlapping
high-resolution patches are then averaged. As discussed
above, this is equivalent to linear convolutions on the
n2 feature maps. If the high-resolution patches used for
reconstruction are of size f3 ×f3, then the linear ﬁlters
have an equivalent spatial support of size f3 ×f3. See
the right part of Figure 3.
The above discussion shows that the sparse-coding-
based SR method can be viewed as a kind of con-
volutional neural network (with a different non-linear
mapping). But not all operations have been considered in
the optimization in the sparse-coding-based SR methods.
On the contrary, in our convolutional neural network,
the low-resolution dictionary, high-resolution dictionary,
non-linear mapping, together with mean subtraction and
averaging, are all involved in the ﬁlters to be optimized.
So our method optimizes an end-to-end mapping that
consists of all operations.
The above analogy can also help us to design hyper-
parameters. For example, we can set the ﬁlter size of
the last layer to be smaller than that of the ﬁrst layer,
and thus we rely more on the central part of the high-
resolution patch (to the extreme, if f3 = 1 , we are
using the center pixel with no averaging). We can also
set n2 < n1 because it is expected to be sparser. A
typical and basic setting is f1 = 9 , f2 = 1 , f3 = 5 ,
n1 = 64 , and n2 = 32 (we evaluate more settings in
the experiment section). On the whole, the estimation
of a high resolution pixel utilizes the information of
(9 + 5 −1)2 = 169 pixels. Clearly, the information
exploited for reconstruction is comparatively larger than
that used in existing external example-based approaches,
e.g., using (5+5 −1)2 = 81 pixels5 [15], [50]. This is one of
the reasons why the SRCNN gives superior performance.
3.3 Training
Learning the end-to-end mapping function F re-
quires the estimation of network parameters Θ =
{W1,W2,W3,B1,B2,B3}. This is achieved through min-
imizing the loss between the reconstructed images
F(Y; Θ) and the corresponding ground truth high-
resolution images X. Given a set of high-resolution
images {Xi} and their corresponding low-resolution
images {Yi}, we use Mean Squared Error (MSE) as the
loss function:
L(Θ) = 1
n
n∑
i=1
||F(Yi; Θ)−Xi||2, (4)
where n is the number of training samples. Using MSE
as the loss function favors a high PSNR. The PSNR
is a widely-used metric for quantitatively evaluating
image restoration quality, and is at least partially related
to the perceptual quality. It is worth noticing that the
convolutional neural networks do not preclude the usage
of other kinds of loss functions, if only the loss functions
are derivable. If a better perceptually motivated metric
is given during training, it is ﬂexible for the network to
adapt to that metric. On the contrary, such a ﬂexibility
is in general difﬁcult to achieve for traditional “hand-
crafted” methods. Despite that the proposed model is
trained favoring a high PSNR, we still observe satisfac-
tory performance when the model is evaluated using
alternative evaluation metrics, e.g., SSIM, MSSIM (see
Section 4.4.1).
The loss is minimized using stochastic gradient de-
scent with the standard backpropagation [28]. In partic-
ular, the weight matrices are updated as
∆i+1 = 0.9 ·∆i −η· ∂L
∂Wℓ
i
, W ℓ
i+1 = Wℓ
i + ∆i+1, (5)
5. The patches are overlapped with 4 pixels at each direction.
6
where ℓ∈{1,2,3}and i are the indices of layers and it-
erations, ηis the learning rate, and ∂L
∂W ℓ
i
is the derivative.
The ﬁlter weights of each layer are initialized by drawing
randomly from a Gaussian distribution with zero mean
and standard deviation 0.001 (and 0 for biases). The
learning rate is 10−4 for the ﬁrst two layers, and 10−5 for
the last layer. We empirically ﬁnd that a smaller learning
rate in the last layer is important for the network to
converge (similar to the denoising case [22]).""",
            """4.3.2 Filter size
In this section, we examine the network sensitivity to
different ﬁlter sizes. In previous experiments, we set
ﬁlter size f1 = 9, f2 = 1 and f3 = 5, and the network
could be denoted as 9-1-5. First, to be consistent with
sparse-coding-based methods, we ﬁx the ﬁlter size of the
second layer to be f2 = 1, and enlarge the ﬁlter size of
other layers to f1 = 11 and f3 = 7 (11-1-7). All the other
6. We use ‘width’ to term the number of ﬁlters in a layer, follow-
ing [17]. The term ‘width’ may have other meanings in the literature.
1 2 3 4 5 6 7 8 9 10
xS10
8
31.5
32
32.5
NumberSofSbackprops
AverageStestSPSNRS(dB)
SRCNNS(9−5−5)
SRCNNS(9−3−5)
SRCNNS(9−1−5)
SCS(31.42SdB)
Fig. 7. A larger ﬁlter size leads to better results.
settings remain the same with Section 4.1. The results
with an upscaling factor 3 on Set5 are 32.57 dB, which is
slightly higher than the 32.52 dB reported in Section 4.1.
This indicates that a reasonably larger ﬁlter size could
grasp richer structural information, which in turn lead
to better results.
Then we further examine networks with a larger ﬁlter
size of the second layer. Speciﬁcally, we ﬁx the ﬁlter size
f1 = 9, f3 = 5, and enlarge the ﬁlter size of the second
layer to be (i) f2 = 3 (9-3-5) and (ii) f2 = 5 (9-5-5).
Convergence curves in Figure 7 show that using a larger
ﬁlter size could signiﬁcantly improve the performance.
Speciﬁcally, the average PSNR values achieved by 9-3-
5 and 9-5-5 on Set5 with 8 ×108 backpropagations are
32.66 dB and 32.75 dB, respectively. The results suggest
that utilizing neighborhood information in the mapping
stage is beneﬁcial.
However, the deployment speed will also decrease
with a larger ﬁlter size. For example, the number of
parameters of 9-1-5, 9-3-5, and 9-5-5 is 8,032, 24,416, and
57,184 respectively. The complexity of 9-5-5 is almost
twice of 9-3-5, but the performance improvement is
marginal. Therefore, the choice of the network scale
should always be a trade-off between performance and
speed.
4.3.3 Number of layers
Recent study by He and Sun [17] suggests that CNN
could beneﬁt from increasing the depth of network
moderately. Here, we try deeper structures by adding
another non-linear mapping layer, which has n22 = 16
ﬁlters with size f22 = 1 . We conduct three controlled
experiments, i.e., 9-1-1-5, 9-3-1-5, 9-5-1-5, which add an
additional layer on 9-1-5, 9-3-5, and 9-5-5, respectively.
The initialization scheme and learning rate of the ad-
ditional layer are the same as the second layer. From
Figures 13(a), 13(b) and 8(c), we can observe that the
four-layer networks converge slower than the three-layer
network. Nevertheless, given enough training time, the
deeper networks will ﬁnally catch up and converge to
the three-layer ones.
The effectiveness of deeper structures for super reso-
lution is found not as apparent as that shown in image
classiﬁcation [17]. Furthermore, we ﬁnd that deeper
networks do not always result in better performance.
Speciﬁcally, if we add an additional layer with n22 = 32
ﬁlters on 9-1-5 network, then the performance degrades
and fails to surpass the three-layer network (see Fig-
ure 9(a)). If we go deeper by adding two non-linear
8
2 4 6 8 10 12
x(10
8
31
31.5
32
32.5
Number(of(backprops
Average(test(PSNR((dB)
SRCNN((9−1−5)
SRCNN((9−1−1−5)
SC((31.42(dB)
(a) 9-1-5 vs. 9-1-1-5
1 2 3 4 5 6 7 8 9 10
xS10
8
31.5
32
32.5
NumberSofSbackprops
AverageStestSPSNRS(dB)
SRCNNS(9−3−5)
SRCNNS(9−3−1−5)
SCS(31.42SdB)
(b) 9-3-5 vs. 9-3-1-5
1 2 3 4 5 6 7 8
xR10
8
31.5
32
32.5
NumberRofRbackprops
AverageRtestRPSNRR(dB)
SRCNNR(9−5−5)
SRCNNR(9−5−1−5)
SCR(31.42RdB)
(c) 9-5-5 vs. 9-5-1-5
Fig. 8. Comparisons between three-layer and four-layer
networks.
mapping layers with n22 = 32 and n23 = 16 ﬁlters on
9-1-5, then we have to set a smaller learning rate to
ensure convergence, but we still do not observe superior
performance after a week of training (see Figure 9(a)).
We also tried to enlarge the ﬁlter size of the additional""",
            """In this paper, we show that the aforementioned
pipeline is equivalent to a deep convolutional neural net-
work [27] (more details in Section 3.2). Motivated by this
fact, we consider a convolutional neural network that
directly learns an end-to-end mapping between low- and
high-resolution images. Our method differs fundamen-
tally from existing external example-based approaches,
in that ours does not explicitly learn the dictionaries [41],
[49], [50] or manifolds [2], [4] for modeling the patch
space. These are implicitly achieved via hidden layers.
Furthermore, the patch extraction and aggregation are
also formulated as convolutional layers, so are involved
in the optimization. In our method, the entire SR pipeline
is fully obtained through learning, with little pre/post-
processing.
We name the proposed model Super-Resolution Con-
volutional Neural Network (SRCNN) 1. The proposed
SRCNN has several appealing properties. First, its struc-
ture is intentionally designed with simplicity in mind,
and yet provides superior accuracy 2 compared with
state-of-the-art example-based methods. Figure 1 shows
a comparison on an example. Second, with moderate
1. The implementation is available at http://mmlab.ie.cuhk.edu.hk/
projects/SRCNN.html.
2. Numerical evaluations by using different metrics such as the Peak
Signal-to-Noise Ratio (PSNR), structure similarity index (SSIM) [43],
multi-scale SSIM [44], information ﬁdelity criterion [38], when the
ground truth images are available.
arXiv:1501.00092v3  [cs.CV]  31 Jul 2015
2
Bicubic / 24.04 dB
SC / 25.58 dBSRCNN / 27.95 dB
Original / PSNR
2 4 6 8 10 12x 108
29.5
30
30.5
31
31.5
32
32.5
33
Number of backprops
Average test PSNR (dB)
SRCNN
SC
Bicubic
Bicubic / 24.04 dB
SC / 25.58 dBSRCNN / 27.95 dB
Original / PSNR
Bicubic / 24.04 dB
SC / 25.58 dBSRCNN / 27.95 dB
Original / PSNR
SRCNN
SC
Bicubic
Bicubic / 24.04 dB
SC / 25.58 dBSRCNN / 27.95 dB
Original / PSNR
Number of backprops
Average test PSNR (dB)
Fig. 1. The proposed Super-Resolution Convolutional
Neural Network (SRCNN) surpasses the bicubic baseline
with just a few training iterations, and outperforms the
sparse-coding-based method (SC) [50] with moderate
training. The performance may be further improved with
more training iterations. More details are provided in
Section 4.4.1 (the Set5 dataset with an upscaling factor
3). The proposed method provides visually appealing
reconstructed image.
numbers of ﬁlters and layers, our method achieves
fast speed for practical on-line usage even on a CPU.
Our method is faster than a number of example-based
methods, because it is fully feed-forward and does
not need to solve any optimization problem on usage.
Third, experiments show that the restoration quality of
the network can be further improved when (i) larger
and more diverse datasets are available, and/or (ii)
a larger and deeper model is used. On the contrary,
larger datasets/models can present challenges for exist-
ing example-based methods. Furthermore, the proposed
network can cope with three channels of color images
simultaneously to achieve improved super-resolution
performance.
Overall, the contributions of this study are mainly in
three aspects:
1) We present a fully convolutional neural net-
work for image super-resolution. The network di-
rectly learns an end-to-end mapping between low-
and high-resolution images, with little pre/post-
processing beyond the optimization.
2) We establish a relationship between our deep-
learning-based SR method and the traditional
sparse-coding-based SR methods. This relationship
provides a guidance for the design of the network
structure.
3) We demonstrate that deep learning is useful in
the classical computer vision problem of super-
resolution, and can achieve good quality and
speed.
A preliminary version of this work was presented
earlier [11]. The present work adds to the initial version
in signiﬁcant ways. Firstly, we improve the SRCNN by
introducing larger ﬁlter size in the non-linear mapping""",
            """1 2 3 4 5 6 7 8
xR10
8
31.5
32
32.5
NumberRofRbackprops
AverageRtestRPSNRR(dB)
SRCNNR(9−5−5)
SRCNNR(9−5−1−5)
SCR(31.42RdB)
(c) 9-5-5 vs. 9-5-1-5
Fig. 8. Comparisons between three-layer and four-layer
networks.
mapping layers with n22 = 32 and n23 = 16 ﬁlters on
9-1-5, then we have to set a smaller learning rate to
ensure convergence, but we still do not observe superior
performance after a week of training (see Figure 9(a)).
We also tried to enlarge the ﬁlter size of the additional
layer to f22 = 3, and explore two deep structures – 9-3-
3-5 and 9-3-3-3. However, from the convergence curves
shown in Figure 9(b), these two networks do not show
better results than the 9-3-1-5 network.
All these experiments indicate that it is not “the deeper
the better” in this deep model for super-resolution. It
may be caused by the difﬁculty of training. Our CNN
network contains no pooling layer or full-connected
layer, thus it is sensitive to the initialization parameters
and learning rate. When we go deeper (e.g., 4 or 5 layers),
we ﬁnd it hard to set appropriate learning rates that
guarantee convergence. Even it converges, the network
may fall into a bad local minimum, and the learned
ﬁlters are of less diversity even given enough training
time. This phenomenon is also observed in [16], where
improper increase of depth leads to accuracy saturation
or degradation for image classiﬁcation. Why “deeper is
not better” is still an open question, which requires in-
vestigations to better understand gradients and training
dynamics in deep architectures. Therefore, we still adopt
three-layer networks in the following experiments.
4.4 Comparisons to State-of-the-Arts
In this section, we show the quantitative and qualitative
results of our method in comparison to state-of-the-art
2 4 6 8 10 12
x(10
8
31
31.5
32
32.5
Number(of(backprops
Average(test(PSNR(=dB)
SRCNN(=9−1−5)
SRCNN(=9−1−1−5,(n 22=16)
SRCNN(=9−1−1−5,(n 22=32)
SRCNN(=9−1−1−1−5,(n 22=32,(n 23=16)
SC(=31.42(dB)
(a) 9-1-1-5 ( n22 = 32) and 9-1-1-1-5 ( n22 = 32, n23 = 16)
1 2 3 4 5 6 7 8 9
xS10
8
31.5
32
32.5
NumberSofSbackprops
AverageStestSPSNRS(dB)
SRCNNS(9−3−5)
SRCNNS(9−3−1−5)
SRCNNS(9−3−3−5)
SRCNNS(9−3−3−3)
SCS(31.42SdB)
(b) 9-3-3-5 and 9-3-3-3
Fig. 9. Deeper structure does not always lead to better
results.
methods. We adopt the model with good performance-
speed trade-off: a three-layer network with f1 = 9, f2 =
5, f3 = 5, n1 = 64, and n2 = 32 trained on the ImageNet.
For each upscaling factor ∈{2,3,4}, we train a speciﬁc
network for that factor 7.
Comparisons. We compare our SRCNN with the state-
of-the-art SR methods:
• SC - sparse coding-based method of Yang et al. [50]
• NE+LLE - neighbour embedding + locally linear
embedding method [4]
• ANR - Anchored Neighbourhood Regression
method [41]
• A+ - Adjusted Anchored Neighbourhood Regres-
sion method [42], and
• KK - the method described in [25], which achieves
the best performance among external example-
based methods, according to the comprehensive
evaluation conducted in Yang et al.’s work [46]
The implementations are all from the publicly available
codes provided by the authors, and all images are down-
sampled using the same bicubic kernel.
Test set.The Set5 [2] (5 images), Set14 [51] (14 images)
and BSD200 [32] (200 images) 8 are used to evaluate the
performance of upscaling factors 2, 3, and 4.
Evaluation metrics. Apart from the widely used PSNR
and SSIM [43] indices, we also adopt another four
evaluation matrices, namely information ﬁdelity cri-
terion (IFC) [38], noise quality measure (NQM) [8],
weighted peak signal-to-noise ratio (WPSNR) and multi-
scale structure similarity index (MSSSIM) [44], which
obtain high correlation with the human perceptual scores
as reported in [46].
4.4.1 Quantitative and qualitative evaluation
As shown in Tables 2, 3 and 4, the proposed SRCNN
yields the highest scores in most evaluation matrices
7. In the area of denoising [3], for each noise level a speciﬁc network
is trained.""",
            """bicubic interpolation. The training falls into a bad local
minimum, due to the inherently different characteristics
of the Y and Cb, Cr channels. (ii) If we pre-train on the
Y or Cb, Cr channels, the performance ﬁnally improves,
but is still not better than “Y only” on the color image
(see the last column of Table 5, where PSNR is computed
(a) First-layer ﬁlters – Cb channel
(b) First-layer ﬁlters – Cr channel
Fig. 13. Chrominance channels of the ﬁrst-layer ﬁlters
using the “Y pre-train” strategy.
in RGB color space). This suggests that the Cb, Cr
channels could decrease the performance of the Y chan-
nel when training is performed in a uniﬁed network.
(iii) We observe that the Cb, Cr channels have higher
PSNR values for “Y pre-train” than for “CbCr pre-train”.
The reason lies on the differences between the Cb, Cr
channels and the Y channel. Visually, the Cb, Cr channels
are more blurry than the Y channel, thus are less affected
by the downsampling process. When we pre-train on
the Cb, Cr channels, there are only a few ﬁlters being
activated. Then the training will soon fall into a bad
local minimum during ﬁne-tuning. On the other hand,
if we pre-train on the Y channel, more ﬁlters will be
activated, and the performance on Cb, Cr channels will
be pushed much higher. Figure 13 shows the Cb, Cr
channels of the ﬁrst-layer ﬁlters with “Y pre-train”, of
which the patterns largely differ from that shown in
Figure 5. (iv) Training on the RGB channels achieves
the best result on the color image. Different from the
YCbCr channels, the RGB channels exhibit high cross-
correlation among each other. The proposed SRCNN
is capable of leveraging such natural correspondences
between the channels for reconstruction. Therefore, the
model achieves comparable result on the Y channel as
“Y only”, and better results on Cb, Cr channels than
bicubic interpolation. (v) In KK [25], super-resolution
is applied on each RGB channel separately. When we
transform its results to YCbCr space, the PSNR value
of Y channel is similar as “Y only”, but that of Cb, Cr
channels are poorer than bicubic interpolation. The result
suggests that the algorithm is biased to the Y channel.
On the whole, our method trained on RGB channels
achieves better performance than KK and the single-
channel network (“Y only”). It is also worth noting that
the improvement compared with the single-channel net-
work is not that signiﬁcant ( i.e., 0.07 dB). This indicates
that the Cb, Cr channels barely help in improving the
performance.
5 C ONCLUSION
We have presented a novel deep learning approach
for single image super-resolution (SR). We show that
conventional sparse-coding-based SR methods can be
12
reformulated into a deep convolutional neural network.
The proposed approach, SRCNN, learns an end-to-end
mapping between low- and high-resolution images, with
little extra pre/post-processing beyond the optimization.
With a lightweight structure, the SRCNN has achieved
superior performance than the state-of-the-art methods.
We conjecture that additional performance can be further
gained by exploring more ﬁlters and different training
strategies. Besides, the proposed structure, with its ad-
vantages of simplicity and robustness, could be applied
to other low-level vision problems, such as image de-
blurring or simultaneous SR+denoising. One could also
investigate a network to cope with different upscaling
factors.
REFERENCES
[1] Aharon, M., Elad, M., Bruckstein, A.: K-SVD: An algorithm for
designing overcomplete dictionaries for sparse representation.
IEEE Transactions on Signal Processing 54(11), 4311–4322 (2006)
[2] Bevilacqua, M., Roumy, A., Guillemot, C., Morel, M.L.A.: Low-
complexity single-image super-resolution based on nonnegative
neighbor embedding. In: British Machine Vision Conference
(2012)
[3] Burger, H.C., Schuler, C.J., Harmeling, S.: Image denoising: Can
plain neural networks compete with BM3D? In: IEEE Conference""",
        ],
    ),
    LLMTestCase(
        input="SRGAN introduces two networks called SRResNet and SRGAN. What is the structural difference between them?",
        actual_output="""SRResNet is a deep residual network (a type of neural network where layers learn residual functions with reference to the layer inputs, instead of learning functions independent of the inputs) optimized for minimizing mean squared error (MSE - a measure of the average squared difference between the estimated values and the actual value). This means it aims to produce images that are, on average, as close as possible to the original high-resolution images at a pixel level.

SRGAN, on the other hand, builds upon the SRResNet architecture but uses a different training approach. It incorporates a generative adversarial network (GAN - a type of machine learning framework composed of two neural networks, a generator and a discriminator, that contest with each other in a zero-sum game framework to learn a task) structure with a perceptual loss function. This loss function combines an adversarial loss (coming from the discriminator in the GAN, which learns to distinguish between real and super-resolved images) and a content loss (which focuses on perceptual similarity by comparing features from a pre-trained VGG network (a convolutional neural network used for image recognition), not just pixel-by-pixel differences). This makes SRGAN focus less on perfect pixel replication and more on producing images that are perceptually similar to the originals, resulting in more realistic textures and details.""",
        expected_output="""Both share the same 16‑block residual generator; SRResNet is trained only with a pixel/feature content loss, whereas SRGAN adds a discriminator and the adversarial term during training, yielding sharper textures.""",
        context=[
            """We employ a deep residual network (SRResNet) … We then train SRGAN, which uses the same generator but adds a discriminator network and optimizes the adversarial loss in addition to the content loss."""
        ],
        retrieval_context=[
            """conﬁrm that SRGAN outperforms all reference methods by
a large margin and sets a new state of the art for photo-
realistic image SR. All differences in MOS ( c.f . Table
2) are highly signiﬁcant on BSD100, except SRCNN vs.
SelfExSR. The distribution of all collected MOS ratings is
summarized in Figure 5.
4. Discussion and future work
We conﬁrmed the superior perceptual performance of
SRGAN using MOS testing. We have further shown that
standard quantitative measures such as PSNR and SSIM
fail to capture and accurately assess image quality with
respect to the human visual system [56]. The focus of this
work was the perceptual quality of super-resolved images
rather than computational efﬁciency. The presented model
is, in contrast to Shi et al. [48], not optimized for video
SR in real-time. However, preliminary experiments on
the network architecture suggest that shallower networks
have the potential to provide very efﬁcient alternatives at
a small reduction of qualitative performance. In contrast to
Dong et al. [10], we found deeper network architectures to
be beneﬁcial. We speculate that the ResNet design has a
substantial impact on the performance of deeper networks.
We found that even deeper networks (B >16) can further
SRResNet SRGAN-MSE SRGAN-VGG22 SRGAN-VGG54 original HR image
Figure 6: SRResNet (left: a,b), SRGAN-MSE (middle left: c,d), SRGAN-VGG2.2 (middle: e,f) and SRGAN-VGG54
(middle right: g,h) reconstruction results and corresponding reference HR image (right: i,j). [ 4×upscaling]
Table 2: Comparison of NN, bicubic, SRCNN [9], SelfExSR [31], DRCN [34], ESPCN [48], SRResNet, SRGAN-VGG54
and the original HR on benchmark data. Highest measures (PSNR [dB], SSIM, MOS) in bold. [4×upscaling]
Set5 nearest bicubic SRCNN SelfExSR DRCN ESPCN SRResNet SRGAN HR
PSNR 26.26 28.43 30.07 30.33 31.52 30.76 32.05 29.40 ∞
SSIM 0.7552 0.8211 0.8627 0.872 0.8938 0.8784 0.9019 0.8472 1
MOS 1.28 1.97 2.57 2.65 3.26 2.89 3.37 3.58 4.32
Set14
PSNR 24.64 25.99 27.18 27.45 28.02 27.66 28.49 26.02 ∞
SSIM 0.7100 0.7486 0.7861 0.7972 0.8074 0.8004 0.8184 0.7397 1
MOS 1.20 1.80 2.26 2.34 2.84 2.52 2.98 3.72 4.32
BSD100
PSNR 25.02 25.94 26.68 26.83 27.21 27.02 27.58 25.16 ∞
SSIM 0.6606 0.6935 0.7291 0.7387 0.7493 0.7442 0.7620 0.6688 1
MOS 1.11 1.47 1.87 1.89 2.12 2.01 2.29 3.56 4.46
increase the performance of SRResNet, however, come at
the cost of longer training and testing times ( c.f . supple-
mentary material). We further found SRGAN variants of
deeper networks are increasingly difﬁcult to train due to the
appearance of high-frequency artifacts.
Of particular importance when aiming for photo-realistic
solutions to the SR problem is the choice of the content loss
as illustrated in Figure 6. In this work, we found lSR
VGG/5.4
to yield the perceptually most convincing results, which
we attribute to the potential of deeper network layers to
represent features of higher abstraction [68, 65, 40] away
from pixel space. We speculate that feature maps of these
deeper layers focus purely on the content while leaving the
adversarial loss focusing on texture details which are the
main difference between the super-resolved images without
the adversarial loss and photo-realistic images. We also
note that the ideal loss function depends on the application.
For example, approaches that hallucinate ﬁner detail might
be less suited for medical applications or surveillance. The
perceptually convincing reconstruction of text or structured
scenes [31] is challenging and part of future work. The
development of content loss functions that describe image
spatial content, but more invariant to changes in pixel space
will further improve photo-realistic image SR results.
5. Conclusion
We have described a deep residual network SRRes-
Net that sets a new state of the art on public benchmark
datasets when evaluated with the widely used PSNR mea-
sure. We have highlighted some limitations of this PSNR-
focused image super-resolution and introduced SRGAN,""",
            """ure 3 where multiple potential solutions with high texture
details are averaged to create a smooth reconstruction.
In Mathieu et al. [42] and Denton et al. [7] the authors
tackled this problem by employing generative adversarial
networks (GANs) [22] for the application of image genera-
tion. Yu and Porikli [66] augment pixel-wise MSE loss with
a discriminator loss to train a network that super-resolves
face images with large upscaling factors ( 8×). GANs
were also used for unsupervised representation learning in
Radford et al. [44]. The idea of using GANs to learn a
mapping from one manifold to another is described by Li
and Wand [38] for style transfer and Yeh et al. [64] for
inpainting. Bruna et al. [5] minimize the squared error in
the feature spaces of VGG19 [49] and scattering networks.
Dosovitskiy and Brox [13] use loss functions based
on Euclidean distances computed in the feature space of
neural networks in combination with adversarial training.
It is shown that the proposed loss allows visually superior
image generation and can be used to solve the ill-posed
inverse problem of decoding nonlinear feature representa-
tions. Similar to this work, Johnson et al. [33] and Bruna
et al. [5] propose the use of features extracted from a pre-
trained VGG network instead of low-level pixel-wise error
measures. Speciﬁcally the authors formulate a loss function
based on the euclidean distance between feature maps
extracted from the VGG19 [49] network. Perceptually more
convincing results were obtained for both super-resolution
and artistic style-transfer [19, 20]. Recently, Li and Wand
[38] also investigated the effect of comparing and blending
patches in pixel or VGG feature space.
1.2. Contribution
GANs provide a powerful framework for generating
plausible-looking natural images with high perceptual qual-
ity. The GAN procedure encourages the reconstructions
to move towards regions of the search space with high
probability of containing photo-realistic images and thus
closer to the natural image manifold as shown in Figure 3.
In this paper we describe the ﬁrst very deep ResNet
[29, 30] architecture using the concept of GANs to form a
perceptual loss function for photo-realistic SISR. Our main
contributions are:
•We set a new state of the art for image SR with
high upscaling factors (4×) as measured by PSNR and
structural similarity (SSIM) with our 16 blocks deep
ResNet (SRResNet) optimized for MSE.
•We propose SRGAN which is a GAN-based network
optimized for a new perceptual loss. Here we replace
the MSE-based content loss with a loss calculated on
feature maps of the VGG network [49], which are
more invariant to changes in pixel space [38].
•We conﬁrm with an extensive mean opinion score
(MOS) test on images from three public benchmark
datasets that SRGAN is the new state of the art, by a
large margin, for the estimation of photo-realistic SR
images with high upscaling factors (4×).
We describe the network architecture and the perceptual
loss in Section 2. A quantitative evaluation on public bench-
mark datasets as well as visual illustrations are provided in
Section 3. The paper concludes with a discussion in Section
4 and concluding remarks in Section 5.
2. Method
In SISR the aim is to estimate a high-resolution, super-
resolved image ISR from a low-resolution input image
ILR. Here ILR is the low-resolution version of its high-
resolution counterpart IHR. The high-resolution images
are only available during training. In training, ILR is
obtained by applying a Gaussian ﬁlter toIHR followed by a
downsampling operation with downsampling factor r. For
an image with C color channels, we describe ILR by a
real-valued tensor of size W ×H ×C and IHR, ISR by
rW ×rH ×Crespectively.
Our ultimate goal is to train a generating function Gthat
estimates for a given LR input image its corresponding HR
counterpart. To achieve this, we train a generator network as
a feed-forward CNN GθG parametrized by θG. Here θG =""",
            """development of content loss functions that describe image
spatial content, but more invariant to changes in pixel space
will further improve photo-realistic image SR results.
5. Conclusion
We have described a deep residual network SRRes-
Net that sets a new state of the art on public benchmark
datasets when evaluated with the widely used PSNR mea-
sure. We have highlighted some limitations of this PSNR-
focused image super-resolution and introduced SRGAN,
which augments the content loss function with an adversar-
ial loss by training a GAN. Using extensive MOS testing,
we have conﬁrmed that SRGAN reconstructions for large
upscaling factors (4×) are, by a considerable margin, more
photo-realistic than reconstructions obtained with state-of-
the-art reference methods.
References
[1] J. Allebach and P. W. Wong. Edge-directed interpolation. InProceed-
ings of International Conference on Image Processing , volume 3,
pages 707–710, 1996. 2
[2] H. A. Aly and E. Dubois. Image up-sampling using total-variation
regularization with a new observation model. IEEE Transactions on
Image Processing, 14(10):1647–1659, 2005. 7
[3] M. Bevilacqua, A. Roumy, C. Guillemot, and M. L. Alberi-Morel.
Low-complexity single-image super-resolution based on nonnegative
neighbor embedding. BMVC, 2012. 6
[4] S. Borman and R. L. Stevenson. Super-Resolution from Image
Sequences - A Review.Midwest Symposium on Circuits and Systems,
pages 374–378, 1998. 2
[5] J. Bruna, P. Sprechmann, and Y . LeCun. Super-resolution with deep
convolutional sufﬁcient statistics. In International Conference on
Learning Representations (ICLR), 2016. 2, 3, 5
[6] D. Dai, R. Timofte, and L. Van Gool. Jointly optimized regressors for
image super-resolution. In Computer Graphics Forum, volume 34,
pages 95–104, 2015. 2
[7] E. Denton, S. Chintala, A. Szlam, and R. Fergus. Deep generative
image models using a laplacian pyramid of adversarial networks. In
Advances in Neural Information Processing Systems (NIPS) , pages
1486–1494, 2015. 3
[8] S. Dieleman, J. Schl ¨uter, C. Raffel, E. Olson, S. K. Snderby,
D. Nouri, D. Maturana, M. Thoma, E. Battenberg, J. Kelly, J. D.
Fauw, M. Heilman, diogo149, B. McFee, H. Weideman, takacsg84,
peterderivaz, Jon, instagibbs, D. K. Rasul, CongLiu, Britefury, and
J. Degrave. Lasagne: First release., 2015. 6
[9] C. Dong, C. C. Loy, K. He, and X. Tang. Learning a deep
convolutional network for image super-resolution. In European
Conference on Computer Vision (ECCV), pages 184–199. Springer,
2014. 3, 6, 8
[10] C. Dong, C. C. Loy, K. He, and X. Tang. Image super-resolution
using deep convolutional networks. IEEE Transactions on Pattern
Analysis and Machine Intelligence, 38(2):295–307, 2016. 3, 5, 7
[11] C. Dong, C. C. Loy, and X. Tang. Accelerating the super-resolution
convolutional neural network. InEuropean Conference on Computer
Vision (ECCV), pages 391–407. Springer, 2016. 3
[12] W. Dong, L. Zhang, G. Shi, and X. Wu. Image deblurring and super-
resolution by adaptive sparse domain selection and adaptive regular-
ization. IEEE Transactions on Image Processing, 20(7):1838–1857,
2011. 2
[13] A. Dosovitskiy and T. Brox. Generating images with perceptual
similarity metrics based on deep networks. In Advances in Neural
Information Processing Systems (NIPS), pages 658–666, 2016. 3
[14] C. E. Duchon. Lanczos Filtering in One and Two Dimensions. In
Journal of Applied Meteorology, volume 18, pages 1016–1022. 1979.
2
[15] S. Farsiu, M. D. Robinson, M. Elad, and P. Milanfar. Fast and
robust multiframe super resolution. IEEE Transactions on Image
Processing, 13(10):1327–1344, 2004. 2
[16] J. A. Ferwerda. Three varieties of realism in computer graphics. In
Electronic Imaging, pages 290–297. International Society for Optics
and Photonics, 2003. 2
[17] W. T. Freeman, T. R. Jones, and E. C. Pasztor. Example-based super-
resolution. IEEE Computer Graphics and Applications, 22(2):56–65,
2002. 2
[18] W. T. Freeman, E. C. Pasztor, and O. T. Carmichael. Learning low-""",
            """Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial
Network
Christian Ledig, Lucas Theis, Ferenc Husz´ar, Jose Caballero, Andrew Cunningham,
Alejandro Acosta, Andrew Aitken, Alykhan Tejani, Johannes Totz, Zehan Wang, Wenzhe Shi
Twitter
{cledig,ltheis,fhuszar,jcaballero,aacostadiaz,aaitken,atejani,jtotz,zehanw,wshi}@twitter.com
Abstract
Despite the breakthroughs in accuracy and speed of
single image super-resolution using faster and deeper con-
volutional neural networks, one central problem remains
largely unsolved: how do we recover the ﬁner texture details
when we super-resolve at large upscaling factors? The
behavior of optimization-based super-resolution methods is
principally driven by the choice of the objective function.
Recent work has largely focused on minimizing the mean
squared reconstruction error. The resulting estimates have
high peak signal-to-noise ratios, but they are often lacking
high-frequency details and are perceptually unsatisfying in
the sense that they fail to match the ﬁdelity expected at
the higher resolution. In this paper, we present SRGAN,
a generative adversarial network (GAN) for image super-
resolution (SR). To our knowledge, it is the ﬁrst framework
capable of inferring photo-realistic natural images for 4×
upscaling factors. To achieve this, we propose a perceptual
loss function which consists of an adversarial loss and a
content loss. The adversarial loss pushes our solution to
the natural image manifold using a discriminator network
that is trained to differentiate between the super-resolved
images and original photo-realistic images. In addition, we
use a content loss motivated by perceptual similarity instead
of similarity in pixel space. Our deep residual network
is able to recover photo-realistic textures from heavily
downsampled images on public benchmarks. An extensive
mean-opinion-score (MOS) test shows hugely signiﬁcant
gains in perceptual quality using SRGAN. The MOS scores
obtained with SRGAN are closer to those of the original
high-resolution images than to those obtained with any
state-of-the-art method.
1. Introduction
The highly challenging task of estimating a high-
resolution (HR) image from its low-resolution (LR)
counterpart is referred to as super-resolution (SR). SR
received substantial attention from within the computer
vision research community and has a wide range of
applications [63, 71, 43].
4×SRGAN (proposed) original
Figure 1: Super-resolved image (left) is almost indistin-
guishable from original (right). [4×upscaling]
The ill-posed nature of the underdetermined SR problem
is particularly pronounced for high upscaling factors, for
which texture detail in the reconstructed SR images is
typically absent. The optimization target of supervised
SR algorithms is commonly the minimization of the mean
squared error (MSE) between the recovered HR image
and the ground truth. This is convenient as minimizing
MSE also maximizes the peak signal-to-noise ratio (PSNR),
which is a common measure used to evaluate and compare
SR algorithms [61]. However, the ability of MSE (and
PSNR) to capture perceptually relevant differences, such
as high texture detail, is very limited as they are deﬁned
based on pixel-wise image differences [60, 58, 26]. This
is illustrated in Figure 2, where highest PSNR does not
necessarily reﬂect the perceptually better SR result. The
1
arXiv:1609.04802v5  [cs.CV]  25 May 2017
bicubic SRResNet SRGAN original
(21.59dB/0.6423) (23.53dB/0.7832) (21.15dB/0.6868)
Figure 2: From left to right: bicubic interpolation, deep residual network optimized for MSE, deep residual generative
adversarial network optimized for a loss more sensitive to human perception, original HR image. Corresponding PSNR and
SSIM are shown in brackets. [4×upscaling]
perceptual difference between the super-resolved and orig-
inal image means that the recovered image is not photo-
realistic as deﬁned by Ferwerda [16].""",
            """and signiﬁcance determined at p< 0.05.
The reader may also be interested in an independently
developed GAN-based solution on GitHub 5. However it
only provides experimental results on a limited set of faces,
which is a more constrained and easier task.
3.2. Training details and parameters
We trained all networks on a NVIDIA Tesla M40 GPU
using a random sample of 350 thousand images from
the ImageNet database [45]. These images are distinct
from the testing images. We obtained the LR images
by downsampling the HR images (BGR, C = 3) using
bicubic kernel with downsampling factor r = 4. For each
mini-batch we crop 16 random 96 ×96 HR sub images
of distinct training images. Note that we can apply the
generator model to images of arbitrary size as it is fully
1https://github.com/xiph/daala (commit: 8d03668)
2https://github.com/jbhuang0604/SelfExSR
3http://cv.snu.ac.kr/research/DRCN/
4https://twitter.box.com/s/
lcue6vlrd01ljkdtdkhmfvk7vtjhetog
5https://github.com/david-gpu/srez
convolutional. We scaled the range of the LR input images
to [0,1] and for the HR images to [−1,1]. The MSE loss
was thus calculated on images of intensity range [−1,1].
VGG feature maps were also rescaled by a factor of 1
12.75
to obtain VGG losses of a scale that is comparable to the
MSE loss. This is equivalent to multiplying Equation 5
with a rescaling factor of ≈ 0.006. For optimization we
use Adam [36] with β1 = 0.9. The SRResNet networks
were trained with a learning rate of 10−4 and 106 update
iterations. We employed the trained MSE-based SRResNet
network as initialization for the generator when training
the actual GAN to avoid undesired local optima. All
SRGAN variants were trained with 105 update iterations
at a learning rate of 10−4 and another 105 iterations at a
lower rate of 10−5. We alternate updates to the generator
and discriminator network, which is equivalent to k = 1
as used in Goodfellow et al. [22]. Our generator network
has 16 identical (B = 16) residual blocks. During test time
we turn batch-normalization update off to obtain an output
that deterministically depends only on the input [32]. Our
implementation is based on Theano [53] and Lasagne [8].
3.3. Mean opinion score (MOS) testing
We have performed a MOS test to quantify the ability of
different approaches to reconstruct perceptually convincing
images. Speciﬁcally, we asked 26 raters to assign an inte-
gral score from 1 (bad quality) to 5 (excellent quality) to the
super-resolved images. The raters rated 12 versions of each
image on Set5, Set14 and BSD100: nearest neighbor (NN),
bicubic, SRCNN [9], SelfExSR [31], DRCN [34], ESPCN
[48], SRResNet-MSE, SRResNet-VGG22∗ (∗not rated on
BSD100), SRGAN-MSE ∗, SRGAN-VGG22 ∗, SRGAN-
VGG54 and the original HR image. Each rater thus rated
1128 instances (12 versions of 19 images plus 9 versions of
100 images) that were presented in a randomized fashion.
The raters were calibrated on the NN (score 1) and HR (5)
versions of 20 images from the BSD300 training set. In a
pilot study we assessed the calibration procedure and the
test-retest reliability of 26 raters on a subset of 10 images
from BSD100 by adding a method’s images twice to a
larger test set. We found good reliability and no signiﬁcant
differences between the ratings of the identical images.
Raters very consistently rated NN interpolated test images
as 1 and the original HR images as 5 (c.f . Figure 5).
The experimental results of the conducted MOS tests are
summarized in Table 1, Table 2 and Figure 5.
3.4. Investigation of content loss
We investigated the effect of different content loss
choices in the perceptual loss for the GAN-based networks.
Speciﬁcally we investigate lSR = lSR
X + 10−3lSR
Gen for the
following content losses lSR
X :
Table 1: Performance of different loss functions for SR-
ResNet and the adversarial networks on Set5 and Set14
benchmark data. MOS score signiﬁcantly higher (p< 0.05)
than with other losses in that category∗. [4×upscaling]
SRResNet- SRGAN-""",
            """3.4. Investigation of content loss
We investigated the effect of different content loss
choices in the perceptual loss for the GAN-based networks.
Speciﬁcally we investigate lSR = lSR
X + 10−3lSR
Gen for the
following content losses lSR
X :
Table 1: Performance of different loss functions for SR-
ResNet and the adversarial networks on Set5 and Set14
benchmark data. MOS score signiﬁcantly higher (p< 0.05)
than with other losses in that category∗. [4×upscaling]
SRResNet- SRGAN-
Set5 MSE VGG22 MSE VGG22 VGG54
PSNR 32.05 30.51 30.64 29.84 29.40
SSIM 0.9019 0.8803 0.8701 0.8468 0.8472
MOS 3.37 3.46 3.77 3.78 3.58
Set14
PSNR 28.49 27.19 26.92 26.44 26.02
SSIM 0.8184 0.7807 0.7611 0.7518 0.7397
MOS 2.98 3.15 ∗ 3.43 3.57 3.72 ∗
•SRGAN-MSE: lSR
MSE, to investigate the adversarial
network with the standard MSE as content loss.
•SRGAN-VGG22: lSR
VGG/2.2 with φ2,2, a loss deﬁned
on feature maps representing lower-level features [68].
•SRGAN-VGG54: lSR
VGG/5.4 with φ5,4, a loss deﬁned
on feature maps of higher level features from deeper
network layers with more potential to focus on the
content of the images [68, 65, 40]. We refer to this
network as SRGAN in the following.
We also evaluate the performance of the generator network
without adversarial component for the two losses lSR
MSE
(SRResNet-MSE) and lSR
VGG/2.2 (SRResNet-VGG22). We
refer to SRResNet-MSE asSRResNet. Note, when training
SRResNet-VGG22 we added an additional total variation
loss with weight 2 ×10−8 to lSR
VGG/2.2 [2, 33]. Quantitative
results are summarized in Table 1 and visual examples
provided in Figure 6. Even combined with the adversarial
loss, MSE provides solutions with the highest PSNR values
that are, however, perceptually rather smooth and less
convincing than results achieved with a loss component
more sensitive to visual perception. This is caused by
competition between the MSE-based content loss and the
adversarial loss. We further attribute minor reconstruction
artifacts, which we observed in a minority of SRGAN-
MSE-based reconstructions, to those competing objectives.
We could not determine a signiﬁcantly best loss function
for SRResNet or SRGAN with respect to MOS score
on Set5. However, SRGAN-VGG54 signiﬁcantly outper-
formed other SRGAN and SRResNet variants on Set14 in
terms of MOS. We observed a trend that using the higher
level VGG feature maps φ5,4 yields better texture detail
when compared to φ2,2 (c.f . Figure 6). Further examples of
perceptual improvements through SRGAN over SRResNet
are provided in the supplementary material.
Figure 5: Color-coded distribution of MOS scores on
BSD100. For each method 2600 samples (100 images ×
26 raters) were assessed. Mean shown as red marker, where
the bins are centered around value i. [4×upscaling]
3.5. Performance of the ﬁnal networks
We compare the performance of SRResNet and SR-
GAN to NN, bicubic interpolation, and four state-of-the-
art methods. Quantitative results are summarized in Table
2 and conﬁrm that SRResNet (in terms of PSNR/SSIM)
sets a new state of the art on three benchmark datasets.
Please note that we used a publicly available framework
for evaluation (c.f . Section 3.1), reported values might thus
slightly deviate from those reported in the original papers.
We further obtained MOS ratings for SRGAN and all
reference methods on BSD100. Examples of images super-
resolved with SRResNet and SRGAN are depicted in the
supplementary material. The results shown in Table 2
conﬁrm that SRGAN outperforms all reference methods by
a large margin and sets a new state of the art for photo-
realistic image SR. All differences in MOS ( c.f . Table
2) are highly signiﬁcant on BSD100, except SRCNN vs.
SelfExSR. The distribution of all collected MOS ratings is
summarized in Figure 5.
4. Discussion and future work
We conﬁrmed the superior perceptual performance of
SRGAN using MOS testing. We have further shown that
standard quantitative measures such as PSNR and SSIM""",
            """(21.59dB/0.6423) (23.53dB/0.7832) (21.15dB/0.6868)
Figure 2: From left to right: bicubic interpolation, deep residual network optimized for MSE, deep residual generative
adversarial network optimized for a loss more sensitive to human perception, original HR image. Corresponding PSNR and
SSIM are shown in brackets. [4×upscaling]
perceptual difference between the super-resolved and orig-
inal image means that the recovered image is not photo-
realistic as deﬁned by Ferwerda [16].
In this work we propose a super-resolution generative
adversarial network (SRGAN) for which we employ a
deep residual network (ResNet) with skip-connection and
diverge from MSE as the sole optimization target. Different
from previous works, we deﬁne a novel perceptual loss us-
ing high-level feature maps of the VGG network [49, 33, 5]
combined with a discriminator that encourages solutions
perceptually hard to distinguish from the HR reference
images. An example photo-realistic image that was super-
resolved with a 4×upscaling factor is shown in Figure 1.
1.1. Related work
1.1.1 Image super-resolution
Recent overview articles on image SR include Nasrollahi
and Moeslund [43] or Yang et al. [61]. Here we will focus
on single image super-resolution (SISR) and will not further
discuss approaches that recover HR images from multiple
images [4, 15].
Prediction-based methods were among the ﬁrst methods
to tackle SISR. While these ﬁltering approaches, e.g. linear,
bicubic or Lanczos [14] ﬁltering, can be very fast, they
oversimplify the SISR problem and usually yield solutions
with overly smooth textures. Methods that put particularly
focus on edge-preservation have been proposed [1, 39].
More powerful approaches aim to establish a complex
mapping between low- and high-resolution image informa-
tion and usually rely on training data. Many methods that
are based on example-pairs rely on LR training patches for
which the corresponding HR counterparts are known. Early
work was presented by Freeman et al. [18, 17]. Related ap-
proaches to the SR problem originate in compressed sensing
[62, 12, 69]. In Glasner et al. [21] the authors exploit patch
redundancies across scales within the image to drive the SR.
This paradigm of self-similarity is also employed in Huang
et al. [31], where self dictionaries are extended by further
allowing for small transformations and shape variations. Gu
et al. [25] proposed a convolutional sparse coding approach
that improves consistency by processing the whole image
rather than overlapping patches.
To reconstruct realistic texture detail while avoiding
edge artifacts, Tai et al. [52] combine an edge-directed SR
algorithm based on a gradient proﬁle prior [50] with the
beneﬁts of learning-based detail synthesis. Zhang et al. [70]
propose a multi-scale dictionary to capture redundancies of
similar image patches at different scales. To super-resolve
landmark images, Yue et al. [67] retrieve correlating HR
images with similar content from the web and propose a
structure-aware matching criterion for alignment.
Neighborhood embedding approaches upsample a LR
image patch by ﬁnding similar LR training patches in a low
dimensional manifold and combining their corresponding
HR patches for reconstruction [54, 55]. In Kim and Kwon
[35] the authors emphasize the tendency of neighborhood
approaches to overﬁt and formulate a more general map of
example pairs using kernel ridge regression. The regression
problem can also be solved with Gaussian process regres-
sion [27], trees [46] or Random Forests [47]. In Dai et al.
[6] a multitude of patch-speciﬁc regressors is learned and
the most appropriate regressors selected during testing.
Recently convolutional neural network (CNN) based SR
algorithms have shown excellent performance. In Wang
et al. [59] the authors encode a sparse representation
prior into their feed-forward network architecture based on
the learned iterative shrinkage and thresholding algorithm""",
            """[70] K. Zhang, X. Gao, D. Tao, and X. Li. Multi-scale dictionary for
single image super-resolution. In IEEE Conference on Computer
Vision and Pattern Recognition (CVPR), pages 1114–1121, 2012. 2
[71] W. Zou and P. C. Yuen. Very Low Resolution Face Recognition
in Parallel Environment . IEEE Transactions on Image Processing,
21:327–340, 2012. 1
A. Supplementary Material
In this supplementary material we ﬁrst brieﬂy investigate the inﬂuence of network depth (number of residual blocks)
on the performance (PSNR, time) of SRResNet in Section A.1. We then visualize on an example image how the SRGAN
network performance evolves with increasing number of training iterations in Section A.2. Results of the MOS tests
conducted on Set5, Set14, BSD100 are summarized in Section A.3. Finally we provide a visualization of all image
reconstruction obtained with SRResNet and SRGAN with a 4×upscaling factor for Set5 (Section A.4), Set14 (Section A.5)
and ﬁve randomly selected images from BSD100 (Section A.6).
Images are best viewed and compared zoomed in. All original low-/high-resolution images and reconstructions
(4×upscaling) obtained with different methods (bicubic, SRResNet-MSE, SRResNet-VGG22, SRGAN-MSE, SRGAN-
VGG22, SRGAN-VGG54) described in the paper are available for download at https://twitter.box.com/s/
lcue6vlrd01ljkdtdkhmfvk7vtjhetog.
A.1. Performance (PSNR/time) vs. network depth
We investigated the inﬂuence of network depth, speciﬁcally the number of residual blocks, on performance (PSNR [dB]
on BSD100 for 4×SR) and inference time [s] of the network architecture described in Figure 4 of the main paper. Time was
assessed on a NVIDIA M40 GPU and averaged over 100 reconstructions of a random low-resolution image with resolution
64×64 with upscaling factor 4×. The measurements are plotted in Figure 7 for a network with (blue) and without (red)
skip-connection. As expected the time of a single forward pass through the network depends approximately linearly on the
number of residual blocks. Whether a skip-connection is used or not has no substantial impact on inference time. However,
we observed substantial gains in performance with the additional skip-connection. We chose a network architecture of
16 residual blocks with skip-connection for the evaluation presented in the main paper as we consider this as good trade-
off between accuracy and speed including training time. While accuracy gains slowly saturate beyond 16 blocks there is,
nevertheless, a clear beneﬁt of using even deeper networks.
Figure 7: Dependence of network performance (PSNR, time) on network depth. PSNR (left) calculated on BSD100. Time
(right) averaged over 100 reconstructions of a random LR image with resolution 64×64.
A.2. Evolution of Generator during SRGAN training
We further investigated how reconstructions of the SRGAN generator network evolve (visually) with increasing number
of training iterations. Visual results obtained after different number of training iterations are illustrated in Figure 8. It is
interesting that after only 20 thousand training iterations the generator substantially diverged from the SRResNet initialization
and produces reconstruction with a lot of high frequency content, including noise. With increasing number of training
iterations reconstructions of the baboon from Set14 appear closer to the reference image. However, there is visually little
change during the last 50-100 thousand update iterations.
SRResNet 20k 40k 60k 80k
100k 140k 180k SRGAN original HR image
Figure 8: Evolution of SRGAN generator network during training progress. Note: Generator initialized with SRResNet
weights; learning rate set to 10−4 for ﬁrst 100k iterations, then reduced to 10−5 for another 100k iterations. [4×upscaling]
A.3. Mean opinion score (MOS) testing
In all conducted MOS tests we have asked 26 human raters to assign a score from 1 (Bad) to 5 (Excellent) to reconstructions""",
        ],
    ),
    # Add more test cases
]
