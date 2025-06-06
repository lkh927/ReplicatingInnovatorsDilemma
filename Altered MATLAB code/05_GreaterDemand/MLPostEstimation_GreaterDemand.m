% Post-estimation exercises with 10000 simulations:
% (1) Show the Values & Policies along the actual history (states).
% (2) Simulate a history (based on the estimated model), and calc the "gap."
% (3) Calculate the Social Welfare outcomes.

load MLEResults_GreaterDemand.mat;
warning off;

% Task (1) Show the Values & Policies along the actual history (states). 

%V = V_out;
%Policy = Policy_out;

V_actual = zeros(18,3);
Policy_actual = zeros(17,5);

for t = 1:18
    
    No = State(t,1);
    Nb = State(t,2);
    Nn = State(t,3);
    
    for type = 1:3
        V_actual(t,type) = V(t,type,No+1,Nb+1,Nn+1);
    end
end

for t = 1:17
    
    No = State(t,1);
    Nb = State(t,2);
    Nn = State(t,3);
    
    for type = 1:5
        Policy_actual(t,type) = Policy(t,type,No+1,Nb+1,Nn+1);
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Task (2) Simulate a history (based on the estimated model), and calc the "gap."

% Initialize
NS = 10000;                     % Number of simulations
npe = 4;                        % Number of potential entrants every year
State_simu = zeros(18,4,NS);    % Simulated history
Adopt_simu = zeros(18,2,NS);    % Simulated innovation decisions
seed = 645456;                  % Seed for random draws
rng(seed);                      % Set seed
U = rand(36+npe,17,NS);             % NS draws from U(0,1) to simulate each firm's discrete choice over 17 years
Uo = U(1:11,:,:);
Ub = U(12:22,:,:);
Un = U(23:36,:,:);
Upe= U(37:40,:,:);
Xo = zeros(11,17,NS);           % Number of exits among old-only firms
Eo = zeros(11,17,NS);           % Number of innovators among old-only firms
Xb = zeros(11,17,NS);           % Number of exits among both
Xn = zeros(14,17,NS);           % Number of exits among new-only
Epe= zeros(npe,17,NS);          % Number of innovators among potential entrants
xo = zeros(17,NS);
eo = zeros(17,NS);
xb = zeros(17,NS);
xn = zeros(17,NS);
epe= zeros(17,NS);

for ns = 1:NS                   % Loop 1: for each simulated history...
    fprintf('\n Simulating history #%5.0f', ns);
    State_simu(1,:,ns) = State(1,:);    % Year 1 is given by data
    State_simu(:,4,ns) = npe*ones(18,1);% N_pe is fixed by assumption    

    for t = 1:17                % Loop 2: for each year
        No = State_simu(t,1,ns);% Current state is given
        Nb = State_simu(t,2,ns);
        Nn = State_simu(t,3,ns);
        Npe = State_simu(t,4,ns);
        
        PrXo = Policy(t,1,No+1,Nb+1,Nn+1);  % Estimated optimal choice probabilities
        PrEo = Policy(t,2,No+1,Nb+1,Nn+1);
        PrXb = Policy(t,3,No+1,Nb+1,Nn+1);
        PrXn = Policy(t,4,No+1,Nb+1,Nn+1);
        PrEpe = Policy(t,5,No+1,Nb+1,Nn+1);
        
        if No > 0
            Xo(1:No,t,ns) = 1*(Uo(1:No,t,ns) < PrXo*ones(No,1));  % Old's exit decision
            xo(t,ns) = sum(Xo(1:No,t,ns),1);                        % Count of old's exits
            Eo(1:No,t,ns) = 1*(Uo(1:No,t,ns) > (1-PrEo)*ones(No,1));% Old's innovation decision
            eo(t,ns) = sum(Eo(1:No,t,ns),1);                        % Count of old's innovations
        else
            xo(t,ns) = 0;
            eo(t,ns) = 0;
        end
        
        if Nb > 0
            Xb(1:Nb,t,ns) = 1*(Ub(1:Nb,t,ns) < PrXb*ones(Nb,1));  % Both's exit decision
            xb(t,ns) = sum(Xb(1:Nb,t,ns),1);                        % Count of both's exits
        else
            xb(t,ns) = 0;
        end
        
        if Nn > 0
            Xn(1:Nn,t,ns) = 1*(Un(1:Nn,t,ns) < PrXn*ones(Nn,1));  % New's exit decision
            xn(t,ns) = sum(Xn(1:Nn,t,ns),1);                        % Count of new's exits
        else
            xn(t,ns) = 0;
        end
        
        if Npe > 0
            Epe(1:Npe,t,ns) = 1*(Upe(1:Npe,t,ns) < PrEpe*ones(Npe,1));% Entrants' innovation
            epe(t,ns) = sum(Epe(1:Npe,t,ns),1);                         % Count of entries
        else
            epe(t,ns) = 0;
        end
        
        State_simu(t+1,1,ns) = No - xo(t,ns) - eo(t,ns);    % No_prime
        State_simu(t+1,2,ns) = Nb - xb(t,ns) + eo(t,ns);    % Nb_prime
        State_simu(t+1,3,ns) = min([14, Nn - xn(t,ns) + epe(t,ns)]);    % Nn_prime (capped at 14)
        Adopt_simu(t+1,1:2,ns) = [eo(t,ns),epe(t,ns)];      % Counts of innovations
    end
end

% Summarize 10,000 simulations into average state evolution and innovations
State_avg = sum(State_simu,3) / NS;     % Average over NS simulated histories
State_avg_rd = round(State_avg);        % Rounding firm counts to integers
Adopt_avg = sum(Adopt_simu,3) / NS;
Adopt_avg_rd = round(Adopt_avg);
Adopt_avg_cumul = zeros(18,2);
for t = 2:18
Adopt_avg_cumul(t,:) = Adopt_avg_cumul(t-1,:) + Adopt_avg(t,:);
end
Adopt_avg_cumul_gap = Adopt_avg_cumul(:,2) - Adopt_avg_cumul(:,1);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Task (3) Calculate the Social Welfare outcomes. ###

% Calculate CS (consumer surplus) in every year & industry state

%fprintf('\n Making Consumer Surplus Matrix (T,No,Nb,Nn)=(18,12,12,15)...\n');
%CS = zeros(18,12,12,15);  % (T x No x Nb x Nn)
%for t = 1:18
%    for n1 = 1:12
%        for n2 = 1:12
%            for n3 = 1:15
%                
%                % Adjustment: Matlab's index starts from 1
%                no = n1 - 1;    
%                nb = n2 - 1;
%                nn = n3 - 1;
%                
                % Prices are determined by the numbers of firms
%                price_old = BigP(t,1,no+1,nb+1,nn+1);
%                price_new = BigP(t,2,no+1,nb+1,nn+1);
%                %price_old = MC(t,1) + (1 / (-alpha1 * (no + nb)));
%                %price_new = MC(t,2) + (1 / (-alpha1 * (nn + nb)));
%                
%                % Deterministic parts of utilities in logit demand system
%                delta_old = alpha0 + alpha1 * price_old + alpha2 * 0  ...
%                            + alpha3 * X(t,1) + Xe(t,1) + Yd(t);
%                delta_new = alpha0 + alpha1 * price_new + alpha2 * 1  ...
%                            + alpha3 * X(t,2) + Xe(t,2) + Yd(t);
                
%                % If a goo
% d doesn't exist, it's not in buyers' choice set
%                if (no + nb) == 0; expDelta_old = 0;    % If Old goods don't exist
%                else expDelta_old = exp(delta_old); end
%                
%                if (nn + nb) == 0; expDelta_new = 0;    % If New goods don't exist
%                else expDelta_new = exp(delta_new); end
%                
%                % Consumer surplus = Market size * Individual CS
%                CS(t,n1,n2,n3) = M(t) * (-1/alpha1) ...
%                                * log(exp(0) + expDelta_old + expDelta_new);

%fprintf('\n Year %2.0f, State (n_old, n_both, n_new) = (%2.0f, %2.0f, %2.0f)',t,no,nb,nn);
%fprintf('\n     CS = %4.2f', CS(t,n1,n2,n3));
%fprintf('\n');

%            end
%        end
%    end
%end

% Calculate PS (producer surplus) in every year & industry state

%fprintf('\n Making Producer Surplus Matrix (T,No,Nb,Nn)=(18,12,12,15)...\n');
%PS = zeros(18,12,12,15);  % (T x No x Nb x Nn)
%for t = 1:18
%    for n1 = 1:12
%        for n2 = 1:12
%            for n3 = 1:15
%                
%                % Adjustment: Matlab's index starts from 1
%                no = n1 - 1;    
%                nb = n2 - 1;
%                nn = n3 - 1;
%                
%                % Profits are determined by the numbers of firms
%                pi_old  = Pi(t,1,n1,n2,n3);
%                pi_both = Pi(t,2,n1,n2,n3);
%                pi_new  = Pi(t,3,n1,n2,n3);
%                
%                % Producer surplus is just the aggregation of firm profits
%                PS(t,n1,n2,n3) = no * pi_old + nb * pi_both + nn * pi_new;
%
%fprintf('\n Year %2.0f, State (n_old, n_both, n_new) = (%2.0f, %2.0f, %2.0f)',t,no,nb,nn);
%fprintf('\n     PS = %4.2f', PS(t,n1,n2,n3));
%fprintf('\n');

%            end
%        end
%    end
%end
%PS = PS * 1000; % Re-scaling (b/c Pi is scaled down by 1000 when solving the model)

% Pick up CS & PS along the simulated history
%fprintf('\n Picking CS & PS along the simulated history... \n');
%CS_simu = zeros(18,1);
%PS_simu = zeros(18,1);
%for t = 1:18
    
%    No = State_avg_rd(t,1);
%    Nb = State_avg_rd(t,2);
%    Nn = State_avg_rd(t,3);
%    
%    CS_simu(t) = CS(t,No+1,Nb+1,Nn+1);
%    PS_simu(t) = PS(t,No+1,Nb+1,Nn+1);
%    
%end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Calculate the Dynamic Costs of Staying & Innovation   %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%fprintf('\n Counting the Dynamic Costs of Staying & Innovation... \n');

% Count the number of active firms along the simulated history
% (Adoptions are already counted in Counterfactual.m as Adopt_simu)
%Adopt_simu2 = Adopt_avg_rd(2:18,1:2); % Watch out! - The timing of counting is different
%for t = 1:17
%        No = State_avg_rd(t,1);
%        Nb = State_avg_rd(t,2);
%        Nn = State_avg_rd(t,3);
%end
%Nactive = sum(State_avg_rd(:,1:3),2);   % Number of active firms

% Multiply # active firms & # adoptions by the cost parameters
%FC_simu = Theta(1) * Nactive;     % Phi x # active firms
%Delta = zeros(17,1);                % (17 x 1) vector of delta
%for t = 1:17
%    Delta(t) = delta^(t-1);
%end
%Kappa_inc = Theta(2) * Delta;       % Multiplier of Adoption Cost (inc)
%Kappa_ent = Theta(3) * Delta;       % Multiplier of Adoption Cost (ent)
%SC_simu = [Kappa_inc .* Adopt_simu2(:,1), Kappa_ent .* Adopt_simu2(:,2)];

% Rescale & collapse across types to summarize
%SC_simu = SC_simu * 1000;
%FC_simu  = FC_simu  * 1000;
%SC_sum = sum(SC_simu,2);
%FC_sum  = sum(FC_simu,2);
%SC_sum = [SC_sum; 0];       % Just add an element for year 18 of Sunk Cost

% Social Welfare
%SW = CS_simu + PS_simu + FC_sum - SC_sum;

% Get the discounted present value of the social welfare (as of 1981)
%Beta = zeros(18,1); % Make a vector of the discount factor
%for t = 1:18
%    Beta(t,1) = beta ^ (t-1);
%end
%SWpv_1981thru98 = Beta' * SW;
%SWpv_from1999   = beta ^ (19 - 1) * (SW(18) / (1 - beta));

% Also get the discounted present value of SW's components
%CS_simu_pv = Beta' * CS_simu;     % PV of Consumer Surplus
%PS_simu_pv = Beta' * PS_simu;     % PV of Producer Surplus
%FC_simu_pv = Beta' * FC_sum;      % PV of Fixed Cost of Operation
%SC_simu_pv = Beta' * SC_sum;      % PV of Sunk Cost of Innovation
%SWpv_1981thru98_ByComponent = [CS_simu_pv, PS_simu_pv, FC_simu_pv, SC_simu_pv];

% Make all-time version of SW accounting by adding "year-19" figures
%Beta2 = zeros(19,1); % Make a vector of the discount factor
%for t = 1:19
%    Beta2(t,1) = beta ^ (t-1);
%end
%CS_simu2 = [CS_simu; CS_simu(18)/(1-beta)];
%PS_simu2 = [PS_simu; PS_simu(18)/(1-beta)];
%FC_simu2 = [FC_sum; FC_sum(18)/(1-beta)];
%SC_simu2 = [SC_sum; SC_sum(18)/(1-beta)];
%SW2 = [CS_simu2, PS_simu2, FC_simu2, -SC_simu2];
%SWpv2 = Beta2' * SW2;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Save & Finish
clear t n1 n2 n3 nb nn no price_old price_new delta_old delta_new...
    expDelta_old expDelta_new pi_old pi_both pi_new PrXo PrXb PrXn...
    No Nb Nn;
save PostEstimation_GreaterDemand.mat ... 
    V_actual Policy_actual... % Output of Task (1)
    State_simu State_avg State_avg_rd... % Output of Task (2)
    Adopt_avg Adopt_avg_rd Adopt_avg_cumul Adopt_avg_cumul_gap...
%    CS PS CS_simu PS_simu FC_simu SC_simu SW ... % Output of Task (3)
%    SWpv_1981thru98 SWpv_from1999 SWpv_1981thru98_ByComponent ...
%    CS_simu2 PS_simu2 FC_simu2 SC_simu2 SW2 SWpv2;
%diary off;
warning on;
