import swr

ds_13a = swr.ds_13a('swr_ds13a.dat')
ds_13a.load_structures()
ds_13a.add_wcd3_2_weirs()
ds_13a.write_structures('swr_ds_13a_meters_ngvd.dat',byreach=True)

#ds_13a.op_2_weir()

m_2_ft = 3.281
ngvd_2_navd = -1.5
mps_2_ftpd = 3.281 * 60.0 * 60.0 * 24.0 
cms_2_cfd = (3.281**3) * 60.0 * 60.0 * 24.0
cms2_2_cfd2 = (3.281**3) * 60.0**2 * 60.0**2 * 24.0**2
lin_istrtype = [5,6,7,8,9]
flux_istrtype = [3]

#ds_13a.filt(5)

ds_13a.scale_offset('strinv',m_2_ft,ngvd_2_navd)
ds_13a.scale_offset('strinv2',m_2_ft,ngvd_2_navd)
ds_13a.scale_offset('strlen',m_2_ft,0.0)

ds_13a.scale_offset('strval',m_2_ft,ngvd_2_navd,istrtype=lin_istrtype)
ds_13a.scale_offset('strval',cms_2_cfd,0.0,istrtype=flux_istrtype)

ds_13a.scale_offset('strwid',m_2_ft,0.0)
ds_13a.scale_offset('strwid2',m_2_ft,0.0)
ds_13a.scale_offset('cstrcrit',m_2_ft,ngvd_2_navd)
ds_13a.scale_offset('strcritc',m_2_ft,0.0)

ds_13a.scale_offset('strrt',mps_2_ftpd,0.0,istrtype=lin_istrtype)
ds_13a.scale_offset('strrt',cms2_2_cfd2,0.0,istrtype=flux_istrtype)
ds_13a.scale_offset('strmax',m_2_ft,0.0,istrtype=lin_istrtype)
ds_13a.scale_offset('strmax',cms_2_cfd,0.0,istrtype=flux_istrtype)


ds_13a.write_structures('swr_ds13a_feet_navd_culverts.dat',byreach=True)
ds_13a.write_ds12('swr_ds12.dat')         