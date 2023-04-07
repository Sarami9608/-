import ConcentDAO2


dao = ConcentDAO2.ConcentDAO()

concentVO = {"CONID":'A0001' , "p_date":'sysdate' , "energy":0, "p_state":0}
dao.insert_Energy(concentVO)
# dao.insert_Predict([concentVO])