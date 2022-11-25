import org.apache.spark.sql.functions._
import org.apache.spark.sql.{Column, DataFrame, SparkSession}
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.DataFrame
import xxxxxxxx val start_date = sc.getConf.get("spark.args.start_date")
def insertHive(spark:SparkSession):Unit= {
  import spark.implicits._
  //提信号
  val arouse_sig_df_3 =spark.sql(
    s"""select * from ilad_ods.ods_vehicle_ xxxxxxxx _event_di 
      where prefix in(‘xx’,’xx’,’xx’) 
      and dt='${start_date}'
      and sig_name 
      in('ESP_VehicleSpeed'
         ,'BCM_PowerMode'
         ,'ACU_LongititudeAcc'
         ,'ADAS_ACCCruiseSpeed'
         ,'ADAS_ACCExitReason'
         ,'ADAS_ xxxxxxxx
         ,'ADAS_ xxxxxxxx
         ,'ADAS_ xxxxxxxx
         ,'ADAS_ xxxxxxxx
         ,'ADAS_ xxxxxxxx
         ,'ADAS_ xxxxxxxx
         ,'ADAS_ xxxxxxxx
         ,'ADAS_ xxxxxxxx
         ,'ADAS_ xxxxxxxx
         ,'ADAS_ xxxxxxxx
         ,'ESP_ xxxxxxxx
         ,'ADAS_ xxxxxxxx
         ,'ESP_ xxxxxxxx
         ,'ESP_ xxxxxxxx
         ,'VCU_CH_ xxxxxxxx
         ,'EPS_ xxxxxxxx
         ,'IPC_ xxxxxxxx
         ,'BCM_ xxxxxxxx
         , xxxxxxxx _ xxxxxxxx
         , xxxxxxxx _ xxxxxxxx
         ,' xxxxxxxx _ xxxxxxxx
         ,'ADAS_ xxxxxxxx)
    """
  ).cache()
  val acc_cycle_status_1 = spark.sql(s"""
    SELECT
        vin,time_start,time_end,acc_start_time,acc_end_time+1 as acc_end_time
    FROM xxxxxxxx
    WHERE dt='${start_date}' and acc_status=1
"""
  ).cache()
  // 过滤信号
  val whole_sigs = arouse_sig_df_3.join(acc_cycle_status_1, Seq("vin"),"right")
    .filter(($"val_start_time"<$"acc_end_time"+5 and $"val_end_time">$"acc_start_time"))
    .withColumn("val_start_time",when($"val_start_time"< $"acc_start_time", $"acc_start_time").otherwise($"val_start_time"))
    .withColumn("val_end_time",when($"val_end_time"> $"acc_end_time"+5, $"acc_end_time"+5).otherwise($"val_end_time"))
    .withColumn("val_dur", $"val_end_time"-$"val_start_time")
  // acc期间信号
  val acc_sig_df_3 = whole_sigs.filter($"val_start_time"<$"acc_end_time")
    .withColumn("val_end_time",when($"val_end_time"> $"acc_end_time", $"acc_end_time").otherwise($"val_end_time"))
    .withColumn("val_dur", $"val_end_time"-$"val_start_time")
  val groupCols = Seq("vin","time_start","time_end","acc_start_time","acc_end_time")
  //ACC循环内急刹车次数
  val WindowSpec = Window.partitionBy("vin", "acc_start_time").orderBy("val_start_time")
  val ACU_ xxxxxxxx _cnt = {acc_sig_df_3.filter(($"sig_name" === "ACU_ xxxxxxxx ") && $"sig_val" < -0.3)
    .withColumn("lag_last_sig_val",$"val_start_time"-lag($"val_end_time", 1,0).over(WindowSpec))
    .filter($"lag_last_sig_val">=10)
    .groupBy("vin","acc_start_time")
    .agg(count($"sig_val").as("ACU_LongititudeAcc_cnt3"))
    .withColumn("acu_longititudeacc_cnt_3",when($"ACU_LongititudeAcc_cnt3".isNull,0).otherwise($"ACU_LongititudeAcc_cnt3"))}
//ACC循环内跟停次数及有效跟停(2.5-5.5米)次数
val pos_w=Window.partitionBy("vin","acc_start_time","acc_end_time").orderBy($"val_start_time".asc)
val Standstill_cycle={
          acc_sig_df_3.filter($"sig_name"==="ESP_ xxxxxxxx ")
          .withColumn("Standstill_or_not",when($"sig_val" <=1, "1")
                                          when( $"sig_val" >1, "2"))
                               .filter($"Standstill_or_not".isNotNull)
            .withColumn("lag_val",lag($"Standstill_or_not",1).over(pos_w))
            .withColumn("lead_val",lead($"Standstill_or_not",1).over(pos_w))
            .filter($"Standstill_or_not"===1)
           .select($"vin",$"arouse_time",$"sleep_time",$"acc_start_time",$"acc_end_time",$"val_start_time",$"val_end_time")
        }
val merge_df={
      Standstill_cycle.withColumn("Standstill_or",$"val_start_time"-lag($"val_end_time",1).over(pos_w))
      .withColumn("tag",when($"Standstill_or">=1,1).otherwise(0.0))
      .withColumn("group",sum($"tag").over(pos_w))
      .groupBy("vin","acc_start_time","acc_end_time","group")
      .agg(min("val_start_time").as("standstill_start"),max("val_end_time").as("standstill_end"))
      .select($"vin",$"acc_start_time",$"acc_end_time",$"standstill_start",$"standstill_end")
    }   
val acc_standstill_cycle = arouse_sig_df_3.join(merge_df, Seq("vin"),"right")
    .filter(($"val_start_time"<$"standstill_end" and $"val_end_time">$"standstill_start"))
    .withColumn("val_start_time",when($"val_start_time"< $"standstill_start", $"standstill_start").otherwise($"standstill_start"))
    .withColumn("val_end_time",when($"val_end_time"> $"standstill_end", $"standstill_end").otherwise($"standstill_end"))
    .withColumn("val_dur", $"val_end_time"-$"val_start_time")
//加入Utils
val groupColsACC = Seq("vin","acc_start_time","acc_end_time","standstill_start","standstill_end")
val StandstillAggItems = Seq(("ADAS_ xxxxxxxx ","Object1Dist",Seq("min")),
                        ("ADAS_ xxxxxxxx ","Object2Dist",Seq("min")),
                        ("ADAS_ xxxxxxxx ","Object3Dist",Seq("min")),
                        ("ADAS_ xxxxxxxx ","Object4Dist",Seq("min")),
                        ("ADAS_RelativeLogitudinalDistToObject5","Object5Dist",Seq("min")),
                        ("ADAS_ xxxxxxxx ","Object6Dist",Seq("min")),
                        ("ADAS_ xxxxxxxx ","Object7Dist",Seq("min")),
                        ("ADAS_ xxxxxxxx ","Object8Dist",Seq("min")),
                        ("ADAS_ xxxxxxxx ","Object9Dist",Seq("min")))
val StandstillSigs = Seq("ADAS_ xxxxxxxx ","ADAS_ xxxxxxxx ","ADAS_ xxxxxxxx ","ADAS_ xxxxxxxx ","ADAS_ xxxxxxxx ","ADAS_ xxxxxxxx ","ADAS_ xxxxxxxx ","ADAS_ xxxxxxxx ","ADAS_ xxxxxxxx ")
val Standstill_df = acc_standstill_cycle.filter($"sig_name".isin(StandstillSigs :_*))
val Standstillmindist = calSigAgg(Standstill_df,  //DF
                          groupColsACC, //groupCols
                          StandstillAggItems)
val partition_cols_standstill = Seq("vin","acc_start_time","acc_end_time","standstill_start","standstill_end")
val pivot_sigs_standstill_cnt = Seq("ADAS_ xxxxxxxx ")
val filled_pivot_df_standstill_cnt = pivotDF(acc_standstill_cycle, partition_cols_standstill, pivot_sigs_standstill_cnt).withColumn("val_dur",col("val_end_time")-col("val_start_time"))
val StandstillWindow=Window.partitionBy("vin","acc_start_time","acc_end_time","standstill_start","standstill_end").orderBy($"val_start_time".asc)
val ACC_cntValidStandStill_2_5 = {filled_pivot_df_standstill_cnt.join(Standstillmindist,Seq("vin","acc_start_time","acc_end_time","standstill_start","standstill_end"),"inner")
                                                                .withColumn("rn",row_number.over(StandstillWindow)).filter($"rn" === 1).drop($"rn") //过滤掉每个跟停循环内多个object id的情况
                                                                .withColumn("acc_cntvalidstandstill_25",when($"ADAS_ xxxxxxxx " === 1, $"Object1Dist_min")
                                                                                                       .when($"ADAS_ xxxxxxxx " === 2, $"Object2Dist_min")
                                                                                                       .when($"ADAS_ xxxxxxxx " === 3, $"Object3Dist_min")
                                                                                                       .when($"ADAS_ xxxxxxxx " === 4, $"Object4Dist_min")
                                                                                                       .when($"ADAS_ xxxxxxxx " === 5, $"Object5Dist_min")
                                                                                                       .when($"ADAS_ xxxxxxxx " === 6, $"Object6Dist_min")
                                                                                                       .when($"ADAS_ xxxxxxxx " === 7, $"Object7Dist_min")
                                                                                                       .when($"ADAS_ xxxxxxxx " === 8, $"Object8Dist_min")
                                                                                                       .when($"ADAS_ xxxxxxxx " === 9, $"Object9Dist_min"))
                                                                                                       .filter($"acc_cntvalidstandstill_25".isNotNull)
                                                                .withColumn("acc_cntvalidstandstill_valid",when($"acc_cntvalidstandstill_25" >=2.5 && $"acc_cntvalidstandstill_25" <=5.5,"valid"))
                                                                .groupBy("vin","acc_start_time") /
                                                                  .agg(count($"acc_cntvalidstandstill_25").as("ACC_cntValidStandStill_all"),
                                                                      count($"acc_cntvalidstandstill_valid").as("ACC_cntValidStandStill_2_5"))}
  //AWB介入+AEB未接入+3秒内加速
  val ACC_point_brake = {acc_sig_df_3.filter((($"sig_name" === "ESP xxxxxxxx xxxxxxxx ") && ($"sig_val" === 1)) || (($"sig_name" === "ESP_ xxxxxxxx ") && ($"sig_val" === 0)) || ($"sig_name" === "VCU_CH_ xxxxxxxx ") && ($"sig_val" > 0))}
  val ACC_point_brake_AEB = ACC_point_brake.filter(($"sig_name" === "ESP_ xxxxxxxx "))
  val ACC_point_brake_AccelPedalPosition = ACC_point_brake.filter(($"sig_name" === "VCU_CH_ xxxxxxxx "))
  val ACC_point_brake_AWB = ACC_point_brake.filter(($"sig_name" === "ESP_ xxxxxxxx "))
  val AWB_AEB_Acceleration_join = {ACC_point_brake_AWB.join(ACC_point_brake_AEB, Seq("vin","acc_start_time"),"inner")
    .filter(((ACC_point_brake_AEB("val_start_time")-ACC_point_brake_AWB("val_start_time"))<= 2) && (ACC_point_brake_AEB("val_start_time") >= ACC_point_brake_AWB("val_start_time")))
    .join(ACC_point_brake_AccelPedalPosition,Seq("vin","acc_start_time"),"inner")
    .filter((ACC_point_brake_AccelPedalPosition("val_start_time")-ACC_point_brake_AEB("val_end_time")<= 3) && (ACC_point_brake_AccelPedalPosition("val_start_time")>= ACC_point_brake_AEB("val_start_time")))
    .groupBy("vin","acc_start_time")
    .agg(countDistinct("acc_start_time").as("AWB_AEB_Acceleration"))}
  val AWB_AEB_no_acce_join = {ACC_point_brake_AWB.join(ACC_point_brake_AEB,Seq("vin","acc_start_time"),"inner")
    .filter(((ACC_point_brake_AEB("val_start_time")-ACC_point_brake_AWB("val_start_time"))<= 2) && (ACC_point_brake_AEB("val_start_time") >= ACC_point_brake_AWB("val_start_time")))
    .groupBy("vin","acc_start_time")
    .agg(count("acc_start_time").as("AWB_AEB"))}
  val ACC_aPrevLon_max_filter = {acc_sig_df_3.withColumn("acc_aprevlon_max_1",when($"sig_name" === "ACU_ xxxxxxxx " && ($"acc_end_time")-($"val_start_time") <=5 && ($"acc_end_time">=$"val_start_time"), $"sig_val"))
    .withColumn("acc_vprevsteang_max_5_1",when($"sig_name" === "EPS_ xxxxxxxx " && ($"acc_end_time")-($"val_start_time") <=5 && ($"acc_end_time">=$"val_start_time"),$"sig_val"))
    .withColumn("LKA_cntActive_during_ACC_1",when($"sig_name" === "ADAS_ xxxxxxxx " && $"sig_val" === 2,$"sig_val"))
    .groupBy("vin","acc_start_time")
    .agg(min($"acc_aprevlon_max_1").as("acc_aprevlon_max"),
      max(abs($"acc_vprevsteang_max_5_1")).as("acc_vprevsteang_max_5"),
      count($"LKA_cntActive_during_ACC_1").as("LKA_cntActive_during_ACC_1"))
    .withColumn("lka_cntactive_during_acc",when($"LKA_cntActive_during_ACC_1".isNull,0).otherwise($"LKA_cntActive_during_ACC_1"))}
  //ACC结束后5秒内最大减速度&&ACC结束后5秒内最大方向盘转角速度
  val ACC_aNextLon_max_filter = {whole_sigs.withColumn("acc_anextlon_max_1",when($"sig_name" === "ACU_ xxxxxxxx " && ($"val_start_time")-($"acc_end_time") <=5 && ($"val_start_time" >= $"acc_end_time"), $"sig_val"))
    .withColumn("acc_anextlon_max_5_1",when($"sig_name" === "EPS_ xxxxxxxx " && ($"val_start_time")-($"acc_end_time") <=5 && ($"val_start_time" >= $"acc_end_time"), $"sig_val"))
    .groupBy("vin","acc_end_time")
    .agg(min($"acc_anextlon_max_1").as("acc_anextlon_max"),
      max(abs($"acc_anextlon_max_5_1")).as("acc_anextlon_max_5"))}
  //加入Running里程
  val running_odometer = spark.sql(s"""
    SELECT
        vin,time_start,time_end,Veh_lenOdo_start,Veh_lenOdo_end
    FROM dw. xxxxxxxx
    WHERE dt='${start_date}'
"""
  )
  val running_sig_df = filterByCycle(arouse_sig_df_3,
    "dw. xxxxxxxx ",
    "time_start",
    "time_end",
    start_date,
    spark)
  //Running循环中ACC不可用信号次数
  val ACC_unavailable = {running_sig_df.filter(($"sig_name" === "ADAS_ xxxxxxxx ") && $"sig_val" =!= 0)
    .groupBy("vin","time_start")
    .agg(count($"sig_val").as("acc_unavailable_cnt"))}
  //Running循环中第一次速度到5和最后一次速度到5的时长
  val Windows = Window.partitionBy("vin", "time_start").orderBy("val_start_time")
  val Windows_last = Window.partitionBy("vin", "time_start").orderBy(desc("val_end_time"))
  val fist_last_time_over_5 = {running_sig_df.filter(($"sig_name" === "ESP_ xxxxxxxx ") && $"sig_val" >= 5)
    .withColumn("first_time",row_number().over(Windows))
    .withColumn("last_time",row_number().over(Windows_last))
    .filter(($"first_time" === 1) || ($"last_time" === 1))
    .groupBy("vin","time_start")
    .agg(min($"val_start_time").as("first_time_over_5"),
      max($"val_end_time").as("last_time_over_5"))}
  //掉包
  val aggItems = Seq(
    ("BCM_ xxxxxxxx ","bcm_ xxxxxxxx ",Seq("tsum")),
    ("RSCM_ xxxxxxxx ","rscm_ xxxxxxxx ",Seq("tsum")),
    ("RSCM_ xxxxxxxx ","rscm_ xxxxxxxx ",Seq("tsum")),
    ("RSCM_ xxxxxxxx ","rscm_strrsbr",Seq("tsum")),
    ("IPC_ xxxxxxxx ","acc_lentotodo",Seq("start","end")), //ACC开始结束里程
    ("ESP_ xxxxxxxx ","acc_average_speed",Seq("tavg")),
    ("ADAS_ xxxxxxxx ","acc_cruise_speed",Seq("tavg")), //ACC循环内平均速度&&ACC期间平均设定车速
    ("ADAS_ xxxxxxxx ","ADAS_ xxxxxxxx ",Seq("min")), //ACC循环内最小车距
    ("ADAS_ xxxxxxxx ","ADAS_ xxxxxxxx ",Seq("min")),
    ("ADAS_ xxxxxxxx ","ADAS_ xxxxxxxx ",Seq("min")),
    ("ADAS_ xxxxxxxx ","ADAS_ xxxxxxxx ",Seq("min")),
    ("ADAS_ xxxxxxxx ","ADAS_ xxxxxxxx ",Seq("min")),
    ("ADAS_ xxxxxxxx ","ADAS_ xxxxxxxx ",Seq("min")),
    ("ADAS_ xxxxxxxx ","ADAS_ xxxxxxxx ",Seq("min")),
    ("ADAS_ xxxxxxxx ","ADAS_ xxxxxxxx ",Seq("min")),
    ("ADAS_ xxxxxxxx ","ADAS_ xxxxxxxx ",Seq("min"))
  )
  val df_part1 = calSigAgg(acc_sig_df_3,groupCols,aggItems)
  val aggItems2 = Seq(("ADAS_ xxxxxxxx ","acc_exit_reason",Seq("max"))   //ACC退出原因
  )
  val df_part2 = calSigAgg(whole_sigs,groupCols,aggItems2)
  val ACC_lenStandStillDist_max_min = {df_part1.withColumn("acc_lendist_min",least($"ADAS_ xxxxxxxx _min",$"ADAS_ xxxxxxxx _min",$"ADAS_ xxxxxxxx _min",$"ADAS_ xxxxxxxx _min",$"ADAS_ xxxxxxxx _min",$"ADAS_ xxxxxxxx _min",$"ADAS_ xxxxxxxx _min",$"ADAS_ xxxxxxxx _min",$"ADAS_ xxxxxxxx _min"))
    .withColumn("cycle_dur",$"acc_end_time"-$"acc_start_time")
    .withColumn("veh_stpsgersbr_val",when($"rscm_stpsgersbr_tsum"/$"cycle_dur">0.5,1.0).otherwise(0.0))
    .withColumn("veh_strlsbr_val",when($"rscm_strlsbr_tsum"/$"cycle_dur">0.5,1.0).otherwise(0.0))
    .withColumn("veh_strrsbr_val",when($"rscm_strrsbr_tsum"/$"cycle_dur">0.5,1.0).otherwise(0.0))
    .join(running_odometer,Seq("vin","time_start","time_end"),"left") 
    .join(ACU_LongititudeAcc_cnt,Seq("vin","acc_start_time"),"left") 
    .join(ACC_cntValidStandStill_2_5,Seq("vin","acc_start_time"),"left")
    .join(AWB_AEB_Acceleration_join,Seq("vin","acc_start_time"),"left") /
    .join(AWB_AEB_no_acce_join,Seq("vin","acc_start_time"),"left") 
    .join(ACC_aPrevLon_max_filter,Seq("vin","acc_start_time"),"left") 
    .join(ACC_aNextLon_max_filter,Seq("vin","acc_end_time"),"left") 
    .join(ACC_unavailable,Seq("vin","time_start"),"left") 
    .join(fist_last_time_over_5,Seq("vin","time_start"),"left") 
    .join(df_part2,Seq("vin","time_start","time_end","acc_start_time","acc_end_time"),"left")
    .select($"vin",$"time_start",$"time_end",$"acc_start_time",$"acc_end_time",($"veh_stpsgersbr_val" + $"veh_strlsbr_val" + $"veh_strrsbr_val" + 1).as("max_passenger"),$"Veh_lenOdo_start".as("run_lentotodo_start"),$"Veh_lenOdo_end".as("run_lentotodo_end"),$"acc_lentotodo_start",$"acc_lentotodo_end",$"acc_exit_reason_max",$"acc_average_speed_tavg",$"acc_cruise_speed_tavg",$"acc_lendist_min",$"acu_longititudeacc_cnt_3", $"lka_cntactive_during_acc",
      $"ACC_cntValidStandStill_2_5".as("acc_cntvalidstandstill_25"), $"AWB_AEB_Acceleration".as("awb_aeb_acceleration"),$"AWB_AEB".as("awb_aeb"),$"acc_aprevlon_max",$"acc_anextlon_max",$"acc_vprevsteang_max_5",$"acc_anextlon_max_5",$"ACC_cntValidStandStill_all".as("acc_cntvalidstandstill_all"),$"acc_unavailable_cnt",($"last_time_over_5"-$"first_time_over_5").as("runningcycl_speed_over_5_duration"))
  }
  ACC_lenStandStillDist_max_min.write.mode("overwrite").parquet(s"/data_ilad/ilad_dw/vehicle/dwd_vehicle_signal xxxxxxxx f_acc_di/dt=${start_date}")
  spark.sql(s"ALTER TABLE ilad_dw.dwd_vehicle_signal_f_acc_di DROP IF EXISTS PARTITION (dt='${start_date}')")
  spark.sql(s"ALTER TABLE ilad_dw.dwd_vehicle_signal_f_acc_di add PARTITION (dt='${start_date}')")
}
try {
  insertHive(spark)
  System.exit(0)
} catch {
  case e:Exception => e.printStackTrace()
    System.exit(1)
}
