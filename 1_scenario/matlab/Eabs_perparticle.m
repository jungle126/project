% 指定 CSV 文件的路径
csv_file_path = 'Dp_Dc_ConcA.csv';
% 读取 CSV 文件数据
data_matrix = csvread(csv_file_path);
%data_matrix说明：
%行固定为3*3*240，第一个三表示场景ABC，第二个三表示三个变量（以此为Dp，Dc，Conc），240为240个时间
%1-720为场景A的数据，721-1440为场景B的数据，1441-2160为场景C的数据
%1-720中，1-240为Dc，一行表示一个时间
%最后需要呈现的结果为三个列表（向量），分别存储场景A，B，C的240小时MAC变化值

%设置n=time=240
n=240;
% 考虑混合态的MAC
MAC_A = zeros(1,n);
% 不考虑混合态的MAC
MAC_EA = zeros(1,n);
% MAC的Eabs
Eabs_A = zeros(1,n);

for i=1:240
    MAC_A(i)=MAC_total(data_matrix(i,:),data_matrix(i+240,:),data_matrix(i+480,:));
    MAC_EA(i)=MAC_total(data_matrix(i+240,:),data_matrix(i+240,:),data_matrix(i+480,:)); %Dc=Dp
end
% 计算Eabs
Eabs_A = MAC_A./MAC_EA;

MAC_ABC_matrix = [MAC_A;MAC_EA;Eabs_A];
csvwrite('MAC_MACE_Rabs_MACEX_ABC_time.csv', MAC_ABC_matrix);