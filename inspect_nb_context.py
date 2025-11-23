from pathlib import Path
p=Path('CW2/CW2_preprocessing.ipynb')
text=p.read_text(encoding='utf-8',errors='replace')
start_markers=['\n     "data": {','\n    "data": {','\n   "data": {','\n"data": {','"data": {']
idx=-1; marker=None
for m in start_markers:
    i=text.find(m)
    if i!=-1:
        idx=i; marker=m; break
print('idx',idx,'marker',repr(marker))
if idx!=-1:
    s=max(0,idx-200)
    e=min(len(text), idx+200)
    print('\n---context around marker---\n')
    print(text[s:e])
    pos_next=text.find('\n   "source": [', idx)
    print('\npos_next',pos_next)
    if pos_next!=-1:
        s2=pos_next
        e2=min(len(text), pos_next+200)
        print('\n---context at next source---\n')
        print(text[s2:e2])
    else:
        print('\nNext 500 chars after idx:')
        print(text[idx:idx+500])
else:
    print('No marker found')
