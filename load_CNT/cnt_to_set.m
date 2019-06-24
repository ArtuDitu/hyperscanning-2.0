%% Workaround: Load .cnt files and convert to/save as .set files %%
% To be able to load with python mne toolbox

% Created on June 24, 2019
% @author: Max Tiessen
% mail: mtiessen@uos.de

%% Load/save CNT files
% add hyperscanning folder to matlab path
addpath(genpath('/net/store/nbp/projects/hyperscanning/'));

% [filepath, filename, setname, eeglabpath, sub] = generate_paths();
cd '/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/load_CNT'
% create new folder for the converted files
mkdir(fullfile(pwd,'set_files'));

% List the pair-nrs. that should be epoched
y = [202] %, 203, 204, 205, 206, 207, 208, 209, 211, 212];

    % Loop over all pair datasets
for i=y
    % set path- and variable-names
    filepath=sprintf('/net/store/nbp/projects/hyperscanning/EEG_data/sub%u/',i);
    filename = sprintf('sub%u.cnt',i);
    setname=filename(1:end-4);

    % load raw EEG data
    raw_EEG = pop_loadeep_v4(fullfile(filepath,filename), 'triggerfile','on');
    % save as set file
    raw_EEG = pop_saveset(raw_EEG, 'filename',setname,'filepath',fullfile(pwd, 'set_files'));
end