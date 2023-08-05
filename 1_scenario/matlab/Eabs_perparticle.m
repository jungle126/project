% ָ�� CSV �ļ���·��
csv_file_path = 'Dp_Dc_ConcA.csv';
% ��ȡ CSV �ļ�����
data_matrix = csvread(csv_file_path);
%data_matrix˵����
%�й̶�Ϊ3*3*240����һ������ʾ����ABC���ڶ�������ʾ�����������Դ�ΪDp��Dc��Conc����240Ϊ240��ʱ��
%1-720Ϊ����A�����ݣ�721-1440Ϊ����B�����ݣ�1441-2160Ϊ����C������
%1-720�У�1-240ΪDc��һ�б�ʾһ��ʱ��
%�����Ҫ���ֵĽ��Ϊ�����б����������ֱ�洢����A��B��C��240СʱMAC�仯ֵ

%����n=time=240
n=240;
% ���ǻ��̬��MAC
MAC_A = zeros(1,n);
% �����ǻ��̬��MAC
MAC_EA = zeros(1,n);
% MAC��Eabs
Eabs_A = zeros(1,n);

for i=1:240
    MAC_A(i)=MAC_total(data_matrix(i,:),data_matrix(i+240,:),data_matrix(i+480,:));
    MAC_EA(i)=MAC_total(data_matrix(i+240,:),data_matrix(i+240,:),data_matrix(i+480,:)); %Dc=Dp
end
% ����Eabs
Eabs_A = MAC_A./MAC_EA;

MAC_ABC_matrix = [MAC_A;MAC_EA;Eabs_A];
csvwrite('MAC_MACE_Rabs_MACEX_ABC_time.csv', MAC_ABC_matrix);