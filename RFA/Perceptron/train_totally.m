load("datos/videos.gz");
 [N,L]=size(data); D=L-1;
ll=unique(data(:,L));
 C=numel(ll);
rand("seed",23); 
b = 0.1;
a = 1;

data=data(randperm(N),:);
[w,E,k]=perceptron(data,b,a);
save_precision(4); save("videos_w","w");
output_precision(2); w