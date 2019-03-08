A = readtable('Nigeria_Ward_smaller_minpop5000_air_migration.txt');
B = readtable('Nigeria_Ward_smaller_minpop5000_local_migration.txt');
allnodes = unique(A.Var1);
mig_mat = zeros(1710, 1710);
[~, ind1] = ismember(A.Var1, allnodes);
[~, ind2] = ismember(A.Var2, allnodes);
inds = sub2ind(size(mig_mat), ind1, ind2);
mig_mat(inds) = A.Var3;
[~, ind1] = ismember(B.Var1, allnodes);
[~, ind2] = ismember(B.Var2, allnodes);
inds = sub2ind(size(mig_mat), ind1, ind2);
mig_mat(inds) = B.Var3;
% sum(mig_mat~=0, 2)
% hist(log10(sum(mig_mat, 1)), 100)
% hist(log10(sum(mig_mat, 2)), 100)
% hist(sum(mig_mat~=0, 1), 100)
% hist(log10(mig_mat), 100)
% hist(log10(mig_mat(mig_mat~=0)), 100)