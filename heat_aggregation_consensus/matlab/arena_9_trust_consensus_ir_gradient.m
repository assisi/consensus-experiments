%% CASU network simulation
clear all;
% Variables definition
n = 9; %Number of node is the network
disp('Trust consensus simulation on 3x3 arena with IR density feedback!');

% - A - adjacency matrix
% - XY - Coordinates in n-by-2 matrix
%Adjacency matrix   9  
A= [0 1 0 1 0 0 0 0 0; 
    1 0 1 0 1 0 0 0 0;
    0 1 0 0 0 1 0 0 0;
    1 0 0 0 1 0 1 0 0;
    0 1 0 1 0 1 0 1 0; %5
    0 0 1 0 1 0 0 0 1;
    0 0 0 1 0 0 0 1 0;
    0 0 0 0 1 0 1 0 1;
    0 0 0 0 0 1 0 1 0; %9
    ];

% Matrix of edges coordinates
XY = [0 0; 1 0; 2 0;
      0 -1; 1 -1; 2 -1;
      0 -2; 1 -2; 2 -2;
      ];

%plot_graph(A,XY);

%% DISCRETE TRUST BASED CONSENSUS ALGORITHM
% Variable definition
s = size(A);
n = s(1);
x0 = zeros(1,n);
%x0 = [1:1:n]; % Initial state of agents
%x0(1:n) = 28;
x0 = [27, 27, 27, 27, 27, 27, 27, 27, 27];
Td = 0.1; % Step size - discretization period
T = 100; % Duration of the simulation
nSteps = T/Td; % Number of steps 
t = [0 : Td : (T-Td)]; % Time
% Memory allocation for nodes state
x = zeros(n, nSteps);
zeta = zeros(n, n, nSteps); % Trust matrix
sigma = zeros(n, n, nSteps); % Confidence matrix
ro = zeros(n, nSteps);  % Agents' performance matrix
teta = zeros(n, n, nSteps);  % Trust observation matrix
x(:,1) = x0; % Copy initial states to states matrix
d = zeros(n,1);
x_ref = zeros(n,1); 
ud = zeros(n,n);
f = zeros(n); % Feedback function - actually is a coverage of IR sensors

%Initial trust matrix %9x9
% a = 0.1;
% zeta(:,:,1) = [1 a 0 a 0 0 0 0 0; 
%     a 1 a 0 a 0 0 0 0;
%     0 a 1 0 0 a 0 0 0;
%     a 0 0 1 a 0 a 0 0;
%     0 a 0 a 1 a 0 a 0; %5
%     0 0 a 0 a 1 0 0 a;
%     0 0 0 a 0 0 1 a 0;
%     0 0 0 0 a 0 a 1 a;
%     0 0 0 0 0 a 0 a 1; %9
%     ];

a = 0.1;
a1 = 0;
zeta(:,:,1) = [a1 a 0 a 0 0 0 0 0; 
    a a1 a 0 a 0 0 0 0;
    0 a a1 0 0 a 0 0 0;
    a 0 0 a1 a 0 a 0 0;
    0 a 0 a a1 a 0 a 0; %5
    0 0 a 0 a a1 0 0 a;
    0 0 0 a 0 0 a1 a 0;
    0 0 0 0 a 0 a a1 a;
    0 0 0 0 0 a 0 a a1; %9
    ];

%Density measurements using IR sensors
f = [6 3 0 0 0 0 0 0 0];
delta = zeros(1,9);
z = zeros(n, nSteps);

for step = 1:(nSteps-1)
    for i = 1:n
        %Calculate the sum of consensus algorithm
        for j = 1:n
            dzeta1 = 0; dzeta2 = 0;
            for k = 1:n
                dzeta1 = dzeta1 + A(i,k)*zeta(i,k,step)*(zeta(k,j,step)-zeta(i,j,step))
                %dzeta1 = dzeta1 + A(i,k)*(zeta(k,j,step)-zeta(i,j,step));
            end
            if i == j % Include sensors measurement                
                dzeta2 = f(i)/6 - zeta(i,i,step)         
            end
            zeta(i,j,step+1) = zeta(i,j,step) + Td*(dzeta1 + dzeta2);
        end
        zeta_max = zeta(i,1,step);
        zeta_max_i = i; zeta_max_j = 1;
        for jj = 2:n
            if(zeta_max < zeta(i,jj,step))
                zeta_max = zeta(i,jj,step);
                zeta_max_i = i; zeta_max_j = jj;
            end
        end
         
        x_ni_max = 0;  %Find the neighbor with max temp
        x_leader_i = 0;
        for j = 1:n
            if((i ==j) && (zeta(i,j,step) == zeta_max))
                %x(i,step+1) = 36;
                x_ref(i) = 36;
                x_leader_i = 1;
            elseif((x_leader_i==0) && (A(i,j)==1) && (x_ni_max < x(j,step)))
                x_ni_max = x(j,step);
                %x(i,step+1) = x_ni_max - 4;
                x_ref(i) = x_ni_max - 4;
                x_i_new = x_ni_max - 4;
            end
        end
        %Limits
        if x_ref(i) < 26
            x_ref(i) = 26;
        end
        if x_ref(i) > 38
            x_ref(i) = 38;
        end
        x(i,step+1) = x(i,step) + 0.1*Td*(x_ref(i) - x(i,step));
%         if x(i,step+1) < 26
%             x(i,step+1) = 26;
%         end
%         if x(i,step+1) > 38
%             x(i,step+1) = 38;
%         end
        
    end
end

%% Plot results
%color = zeros(3,9);
%color(:,1) = [1,0,0];
%color(:,2) = [0,1,0];
%color(:,3) = [0,0,1];
%color(:,4) = [240,150,60] / 255;
%color(:,5) = [1,0,1];
%color(:,6) = [0,1,1];
%color(:,7) = [25,70,85] / 255;
%color(:,8) = [207,165,80] / 255;
%color(:,9) = [200,40,50] / 255;
%
%fig = figure; %set(fig1, 'Position', get(0,'Screensize')); % Maximize figure.
%col1 = [1,0,0];
%plot(t, x(1,:), 'Color', color(:,1), 'LineWidth', 2);
%hold on; grid on;
%xlabel('t (s)'); ylabel('Stanje');
%title('Stanja CASU jedinica');
%legendInfo{1} = ['x_1'];
%for i = 2:n
%    col = randi([0 255],1,3);
%    col = col/255;
%    plot(t, x(i,:), 'Color', color(:,i), 'LineWidth', 2);
%    legendInfo{i} = ['x_{' num2str(i) '}'];
%end
%legend(legendInfo);
%%saveas(fig, 'ex1_states_gradient2', 'png');
%
%
%%set(gca,'FontSize',28); %Set font size
%% 
%%Plot nodes' trust converted in temperature reference
%fig = figure; %set(fig1, 'Position', get(0,'Screensize')); % Maximize figure.
%col1 = [1,0,0];
%k = 1;  %Node ID
%z(1,:) =  zeta(k,k,:);%zeta(k,k,:)*10 + 26;
%plot(t, z(1,:), 'Color', color(:,1), 'LineWidth', 2);
%hold on; grid on;
%xlabel('t (s)'); ylabel('Zeta');
%title('Trust value');
%legendInfo{1} = ['\zeta_{' num2str(k) '1}'];
%for i = 2:n
%    col = randi([0 255],1,3);
%    col = col/255;
%    z(1,:) = zeta(i,i,:);
%    plot(t, z(1,:), 'Color', color(:,i), 'LineWidth', 2);
%    legendInfo{i} = ['\zeta_{' num2str(i) num2str(i) '}'];
%end
%legend(legendInfo);
%%saveas(fig, 'ex1_trust_11', 'png');
%
%% 
%%Delta 1
%% fig = figure; %set(fig1, 'Position', get(0,'Screensize')); % Maximize figure.
%% col1 = [1,0,0];
%% plot(t, z(1,:), 'Color', col1, 'LineWidth', 2);
%% hold on; grid on;
%% xlabel('t (s)'); ylabel('Stanje');
%% title('z CASU jedinica');
%% legendInfo3{1} = ['z_1'];
%% for i = 2:n
%%     col = randi([0 255],1,3);
%%     col = col/255;
%%     plot(t, z(i,:), 'Color', col, 'LineWidth', 2);
%%     legendInfo3{i} = ['z_{' num2str(i) '}'];
%% end
%% legend(legendInfo3);
%
%%Plot trust values
%fig = figure; %set(fig, 'Position', get(0,'Screensize')); % Maximize figure.
%k = 1;  %Node ID
%z(1,:) = zeta(k,1,:);
%plot(t, z(1,:), 'Color', color(:,1), 'LineWidth', 2);
%hold on; grid on;
%xlabel('t (s)'); ylabel('Zeta');
%title('Trust value');
%legendInfo{1} = ['\zeta_{' num2str(k) '1}'];
%for i = 2:n
%    z(1,:) = zeta(k,i,:);
%    plot(t, z(1,:), 'Color', color(:,i), 'LineWidth', 2);
%    legendInfo{i} = ['\zeta_{' num2str(k) num2str(i) '}'];
%end
%legend(legendInfo);
%%saveas(fig, 'ex1_trust_1i_con2', 'png');

% %Agent 2 trust value
% nagent = 2;
% fig3 = figure; %set(fig1, 'Position', get(0,'Screensize')); % Maximize figure.
% col1 = [1,0,0];
% z(1,:) = zeta(nagent,nagent,:);
% plot(t, z(1,:), 'Color', col1, 'LineWidth', 2);
% hold on; grid off;
% xlabel('t (s)'); ylabel('Zeta');
% title('Trust value');
% 
% for i = 2:n
%     col = randi([0 255],1,3);
%     col = col/255;
%     z(1,:) = zeta(nagent,i,:);
%     plot(t, z(1,:), 'Color', col, 'LineWidth', 2);
% end
