import matplotlib.pyplot as plt
import numpy as np
import math
from sklearn.preprocessing import StandardScaler

def plot_fhr_trace(fhr,ground_truth_fhr,fhr_trace_er_length,fs,results,width=15):
  '''
  This function takes in a signal and plot only a part of it. It also plots the
  ECG annotations.
  E.g.
  If sections=5 and section_n=2 this function will divide the signal
  into 5 sections and prints only the second one
  '''
  plt.rcParams['figure.figsize'] = [width, 1.5]
  plt.rcParams['lines.linewidth'] = 0.5
  results = [[str(results[0]),str(round(results[1],2)),str(round(results[2],2)),str(round(results[3],2))+"%"]]
  #plt.figure(figsize=(width,0.6))
  section_length = len(fhr)
  start = 0
  end = (start+section_length) -1

  xaxis = np.array(range(start,end))
  xaxis = xaxis/fs

  fig, (ax1, ax2) = plt.subplots(2)
  ax1.table( 
      cellText = results,  
      colLabels = ['Sample n°','RMSE', 'Max Error','Out of range'], 
      cellLoc ='center',  
      loc ='upper center')
  ax1.set_axis_off()
  ax2.set_ylabel("Bpm")
  ax2.plot(xaxis,fhr[start:end],label="Detected FHR", color="r")
  ax2.plot(xaxis,ground_truth_fhr[start:end],label="Real FHR", color="blue")
  ax2.set_xlabel("Time (s)")
  val_max = max(max(fhr),max(ground_truth_fhr))
  val_min = min(min(fhr),min(ground_truth_fhr))
  ax2.fill_between(np.linspace(0,60,len(fhr_trace_er_length)), val_min, val_max, where=fhr_trace_er_length==True, alpha=0.1,color="r",label="Out of range")
  ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.9),fancybox=True, ncol=5)
  return

def plot_error_timeline(signal,annotations,fs,results,ground_truth,section_n=0,sections=1,width=15):

  if section_n >= sections:
    print("Error: section_n > sections")
    return
  
  section_length = round(len(signal)/sections)
  start = section_n * section_length
  end = (start+section_length) -1
  if end > len(signal)-1:
    end = len(signal)-1

  if len(ground_truth) > 0:
    gt_pos = []
    gt_val = []
    for g in ground_truth:
      if g > end:
        break
      elif g < start:
        continue
      else:
        gt_pos.append(g/fs)

  ann_pos = []
  for a in annotations:
    if a > end:
      break
    elif a < start:
      continue
    else:
      ann_pos.append(a/fs)

  xaxis = np.array(range(start,end))
  xaxis = xaxis/fs

  plt.rcParams['figure.figsize'] = [width, 1.5]

  fig, (ax1, ax2) = plt.subplots(2)
  ax1.table( 
    cellText = [results],
    colLabels = ['Sample_ID','Window size (ms)','N° of beats','N° of matches', 'Performance (%)','RMSE', 'Mean (ms)', 'Std Dev (ms)'], 
    cellLoc ='center',  
    loc ='upper center')
  ax1.set_axis_off()
  
  is_first = True # To add only one label to the legend
  for line in ann_pos:
      if is_first:
        ax2.axvline(x=line, color = "green", linestyle = 'solid',linewidth = "1",label='Matched beats')
        is_first = False
      else:
        ax2.axvline(x=line, color = "green", linestyle = 'solid',linewidth = "1")

  is_first = True # To add only one label to the legend
  if len(ground_truth) > 0:
    for line in gt_pos:
      if is_first:
        ax2.axvline(x=line, color = 'red', linestyle = 'solid',linewidth = '1',label='Unmatched beats')
        is_first = False
      else:
        ax2.axvline(x=line, color = 'red', linestyle = 'solid',linewidth = '1')

  ax2.tick_params(
    axis='y',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    left=False,      # ticks along the bottom edge are off
    labelleft=False)
  
  ax2.plot(xaxis,signal[start:end],label="ECG signal")
  ax2.set_xlabel("Time (s)")
  ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.9),fancybox=True, ncol=5)
  return

def plot_signal_annotations(signal,annotations,fs,section_n=0,sections=1,ground_truth=[],annotation_symbol=[],ground_truth_symbol=[],signal_label="ECG signal",width=15):
  '''
  This function takes in a signal and plot only a part of it. It also plots the
  ECG annotations.
  E.g.
  If sections=5 and section_n=2 this function will divide the signal
  into 5 sections and prints only the second one
  '''

  if section_n >= sections:
    print("Error: section_n > sections")
    return
  section_length = round(len(signal)/sections)
  start = section_n * section_length
  end = (start+section_length) -1
  if end > len(signal)-1:
    end = len(signal)-1

  if len(ground_truth) > 0:
    gt_pos = []
    gt_val = []
    for g in ground_truth:
      if g > end:
        break
      elif g < start:
        continue
      else:
        gt_pos.append(g/fs)
        gt_val.append(signal[g])

  ann_pos = []
  ann_val = []
  for a in annotations:
    if a > end:
      break
    elif a < start:
      continue
    else:
      ann_pos.append(a/fs)
      ann_val.append(signal[a])

  xaxis = np.array(range(start,end))
  xaxis = xaxis/fs

  if len(annotation_symbol) > 2:
    ann_marker = annotation_symbol[0]
    ann_color = annotation_symbol[1]
    ann_label = annotation_symbol[2]
  elif len(annotation_symbol) > 0:
    ann_marker = annotation_symbol[0]
    ann_color = annotation_symbol[1]
    ann_label = "Detected beats"
  else:    
    ann_marker = 'o'
    ann_color = 'red'
    ann_label = "Detected beats"

  plt.rcParams['figure.figsize'] = [width, 1.5]
  plt.rcParams['lines.linewidth'] = 0.5

  if len(ann_pos) > 0:
    plt.scatter(ann_pos,ann_val,marker=ann_marker,c=ann_color,label=ann_label)

  if len(ground_truth_symbol) > 0:
    gt_linestyle = ground_truth_symbol[0]
    gt_color = ground_truth_symbol[1]
    gt_linewidth = ground_truth_symbol[2]
  else:    
    gt_linestyle = 'dotted'
    gt_color = 'g'
    gt_linewidth = '2'
  
  if len(ground_truth) > 0:
    is_first = True
    for line in gt_pos:
      if is_first:
        plt.axvline(x=line, color = gt_color, linestyle = gt_linestyle,linewidth = gt_linewidth,label="Annotated beats",alpha=0.5)
        is_first = False
      else:
        plt.axvline(x=line, color = gt_color, linestyle = gt_linestyle,linewidth = gt_linewidth,alpha=0.5)

  
  plt.xlabel("Time (s)")
  plt.ylabel("Amplitude (uV)")
  plt.plot(xaxis,signal[start:end],label=signal_label)
  plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.4),fancybox=True, ncol=5)
  plt.show()
  return

def plot_signal(signal_combo,fs,section_n=0,sections=1,width=15,signal_type="ECG signal",signals_labels=None,different_sig=None,row_height=1.5):

  '''
  This function takes in a signal and plot only a part of it.
  E.g.
  If sections=5 and section_n=2 this function will divide the signal
  into 5 sections and prints only the second one

  signal_labels are labels for the y axis
  signal_type is the type printed in the legend
  different_signal is for the signal to be printed different:
  -index
  -color
  -type of signal for the legend
  -label for y axis
  '''
  if signals_labels is None: 
    signals_labels = []
  if different_sig is None: 
    different_sig = []
  signal = signal_combo.copy()

  if section_n >= sections:
      print("Error: section_n > sections")
      return
  
  if signal.ndim > 1:
    if signal.shape[0] == 1:
        signal = signal[0]
        rows = 1
    else:
        rows = signal.shape[0]
  else:
    rows = 1

  plt.rcParams['figure.figsize'] = [width, 1.5]
  plt.rcParams['lines.linewidth'] = 0.5

  f, ax = plt.subplots(rows, sharex=True)
  f.set_figwidth(width)
  f.set_figheight(row_height*rows)

  l = []
  l_name = []

  if len(signals_labels) == 0:
    for i in range(0,rows):
      signals_labels.append("Signal " + str(i+1))
          
  is_first = True
  for i in range(0,rows):
    if rows > 1:
        sig = signal[i]
    else:
        sig = signal
    section_length = round(len(sig)/sections)
    start = section_n * section_length
    end = (start+section_length) -1
    if end > len(sig)-1:
        end = len(sig)-1
    xaxis = np.array(range(start,end))
    xaxis = xaxis/fs
    if rows > 1:
      ax[i].set_ylabel(signals_labels[i])
    else:
      ax.set_ylabel(signals_labels[i])
    if len(different_sig) > 0 and i in different_sig[0]:
      l1, = ax[i].plot(xaxis,sig[start:end],color=different_sig[1])
      ax[i].set_ylabel(different_sig[3])
      l.append(l1)
      l_name.append(different_sig[2])
    else:
      if rows > 1:
        l1, = ax[i].plot(xaxis,sig[start:end])
      else:
        l1, = ax.plot(xaxis,sig[start:end])
      if is_first:
        l_name.append(signal_type)
        l.append(l1)
        is_first = False

  f.tight_layout()
  plt.xlabel("Time (s)")
  plt.legend(l,l_name,loc='upper center', bbox_to_anchor=(0.5, -0.4),fancybox=True, ncol=5)
  plt.show()
  return