from bro import flow,seawat

f_flow,f_seawat = open('grid\\'+flow.root+'.spc','w',0),open('grid\\'+seawat.root+'.spc','w',0)

f_flow.write('{0:6d} {1:6d}\n'.format(flow.nrow,flow.ncol))
f_seawat.write('{0:6d} {1:6d}\n'.format(seawat.nrow,seawat.ncol))

f_flow.write('{0:20.8G} {1:20.8G} 0.0\n'.format(flow.offset[0],flow.offset[1]+(flow.nrow*flow.delc)))
f_seawat.write('{0:20.8G} {1:20.8G} 0.0\n'.format(seawat.offset[0],seawat.offset[1]+(seawat.nrow*seawat.delc)))

f_flow.write(str(flow.ncol)+'*'+str(flow.delr)+'\n')
f_seawat.write(str(seawat.ncol)+'*'+str(seawat.delr)+'\n')

f_flow.write(str(flow.nrow)+'*'+str(flow.delc)+'\n')
f_seawat.write(str(seawat.nrow)+'*'+str(seawat.delc)+'\n')

f_flow.close()
f_seawat.close()
