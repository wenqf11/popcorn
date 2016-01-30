package cn.edu.tsinghua.thss.popcorn.ui;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.view.ViewPager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import cn.edu.tsinghua.thss.popcorn.AttendanceActivity;
import cn.edu.tsinghua.thss.popcorn.BonusActivity;
import cn.edu.tsinghua.thss.popcorn.DeviceInfoSearchActivity;
import cn.edu.tsinghua.thss.popcorn.MaintainListActivity;
import cn.edu.tsinghua.thss.popcorn.R;
import cn.edu.tsinghua.thss.popcorn.RankActivity;
import cn.edu.tsinghua.thss.popcorn.RepairListActivity;
import cn.edu.tsinghua.thss.popcorn.RepairRecordActivity;
import cn.edu.tsinghua.thss.popcorn.TaskActivity;
import cn.edu.tsinghua.thss.popcorn.TaskListActivity;

/**
 * @author wenqingfu
 * @email thssvince@163.com
 * @date 2015.04.12
 */
public class AppsFragment extends Fragment {

    private View appsView;

    @Override
    public View onCreateView(LayoutInflater inflater,ViewGroup container,Bundle savedInstanceState){
        super.onCreateView(inflater, container, savedInstanceState);
        if (appsView == null) {
            appsView = inflater.inflate(R.layout.activity_tab_apps, container,false);
        }
        //缓存的rootView需要判断是否已经被加过parent， 如果有parent需要从parent删除，要不然会发生这个rootview已经有parent的错误。
        ViewGroup parent = (ViewGroup) appsView.getParent();
        if (parent != null) {
            parent.removeView(appsView);
        }
        //考勤打卡
        View mAppsAttendanceLayout = appsView.findViewById(R.id.id_apps_attendance_ll);
        mAppsAttendanceLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent=new Intent(getActivity(), AttendanceActivity.class);
                Bundle bundle=new Bundle();
                intent.putExtras(bundle);
                startActivity(intent);
            }
        });

        //抄表
        View mAppsRecordLayout = appsView.findViewById(R.id.id_apps_record_ll);
        TextView mBodyMeterTv = (TextView)mAppsRecordLayout.findViewById(R.id.main_body_app_meter_id);
        mBodyMeterTv.setVisibility(View.GONE);
        mAppsRecordLayout.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v) {
                ViewPager vg = (ViewPager) getActivity()
                        .findViewById(R.id.id_page_vp);
                vg.setCurrentItem(1, false);
            }
        });


        //报修
        View mAppsReportLayout = appsView.findViewById(R.id.id_apps_report_ll);
        mAppsReportLayout.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v) {
                ViewPager vg = (ViewPager) getActivity()
                        .findViewById(R.id.id_page_vp);
                vg.setCurrentItem(2, false);
            }
        });

        //保养
        View mAppsMaintainLayout = appsView.findViewById(R.id.id_apps_maintain_ll);
        mAppsMaintainLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent=new Intent(getActivity(), MaintainListActivity.class);
                Bundle bundle=new Bundle();
                intent.putExtras(bundle);
                startActivity(intent);
            }
        });

        //维修
        View mAppsRepairLayout = appsView.findViewById(R.id.id_apps_repair_ll);
        mAppsRepairLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent=new Intent(getActivity(), RepairListActivity.class);
                Bundle bundle=new Bundle();
                intent.putExtras(bundle);
                startActivity(intent);
            }
        });

        //设备资料
        View mAppsDeviceInfoLayout = appsView.findViewById(R.id.id_apps_deviceInfo_ll);
        mAppsDeviceInfoLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent=new Intent(getActivity(), DeviceInfoSearchActivity.class);
                Bundle bundle=new Bundle();
                intent.putExtras(bundle);
                startActivity(intent);
            }
        });

        //积分排名
        View mAppsRankLayout = appsView.findViewById(R.id.id_apps_rank_ll);
        mAppsRankLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent=new Intent(getActivity(), RankActivity.class);
                Bundle bundle=new Bundle();
                intent.putExtras(bundle);
                startActivity(intent);
            }
        });


        //抢彩蛋
        View mAppsBonusLayout = appsView.findViewById(R.id.id_apps_bonus_ll);
        mAppsBonusLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent=new Intent(getActivity(), BonusActivity.class);
                Bundle bundle=new Bundle();
                intent.putExtras(bundle);
                startActivity(intent);
            }
        });

        //维修记录
        View mAppsRepairRecordLayout = appsView.findViewById(R.id.main_body_app_repair_record);
        mAppsRepairRecordLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent=new Intent(getActivity(), RepairRecordActivity.class);
                Bundle bundle=new Bundle();
                intent.putExtras(bundle);
                startActivity(intent);
            }
        });

        //任务
        View mAppsTaskLayout = appsView.findViewById(R.id.id_apps_task_ll);
        mAppsTaskLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent=new Intent(getActivity(), TaskListActivity.class);
                Bundle bundle=new Bundle();
                intent.putExtras(bundle);
                startActivity(intent);
            }
        });

        return appsView;
    }


    @Override
    public void onActivityCreated(Bundle savedInstanceState){
        super.onActivityCreated(savedInstanceState);
    }
}