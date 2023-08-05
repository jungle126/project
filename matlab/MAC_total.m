function MAC = MAC_total(Dp_list,Dc_list,Conc_list)
%MAC_TOTAL 计算一个时刻population的MAC值
%   此处显示详细说明
RI_BC= complex(1.85,0.71); 
RI_shell= complex(1.53,0);
BC_den= 1800;
wavelength = 550*1e-9;
Dp_m = Dp_list*1e-9;
Dc_m = Dc_list*1e-9;
for j=1:length(Dc_m)
    xcor = pi*Dc_m(j)/wavelength;
    xman = pi*Dp_m(j)/wavelength;
    result=Miecoated(RI_BC,RI_shell,xcor,xman,1);
    qabs=result(3);
    cabs_shell(j)=1/4*pi*Dp_m(j).^2 * qabs * Conc_list(j);
    mass_bc(j)=1/6*pi*Dc_m(j).^3 * BC_den * Conc_list(j);
end
MAC = sum(cabs_shell)/sum(mass_bc)*1e-3;


