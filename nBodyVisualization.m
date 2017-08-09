load('data.mat')
plt = plot3(data(1, :, 1), data(2, :, 1), data(3, :, 1), '.');
for ii=1:1000
    set(gca,'Color','k')
    set(gcf,'units','points','position',[0,0,1900,1000])
    set(gcf, 'Color', 'k')
    set(plt, 'xdata', data(1, :, ii), 'ydata', data(2, :, ii), 'zdata', data(3, :, ii));
    axis manual
    xlim([0, 1500])
    ylim([0, 1500])
    zlim([0, 1000])
    drawnow
    F(ii) = getframe(gcf)
    pause(0.1)
end

video = VideoWriter('nBody.avi');
open(video);
writeVideo(video, F)
close(video)
