package cn.edu.tsinghua.thss.popcorn.ui;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.view.ViewPager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import cn.edu.tsinghua.thss.popcorn.AttendanceActivity;
import cn.edu.tsinghua.thss.popcorn.R;

/**
 * @author wenqingfu
 * @email thssvince@163.com
 * @date 2015.04.12
 */
public class AppsFragment extends Fragment {

    @Override
    public View onCreateView(LayoutInflater inflater,ViewGroup container,Bundle savedInstanceState){
        super.onCreateView(inflater, container, savedInstanceState);
        View appsView = inflater.inflate(R.layout.activity_tab_apps, container,false);

        //考勤打卡
        View mAppsAttendanceLayout = appsView.findViewById(R.id.id_apps_attendance_ll);
        mAppsAttendanceLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent=new Intent(getActivity(), AttendanceActivity.class);
                Bundle bundle=new Bundle();
                intent.putExtras(bundle);
                //执行意图
                startActivity(intent);
            }
        });

        //抄表
        View mAppsRecordLayout = appsView.findViewById(R.id.id_apps_record_ll);
        mAppsRecordLayout.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v) {
                ViewPager vg = (ViewPager) getActivity()
                        .findViewById(R.id.id_page_vp);
                vg.setCurrentItem(1, false);
            }
        });


        //维修
        View mAppsRepairLayout = appsView.findViewById(R.id.id_apps_repair_ll);
        mAppsRepairLayout.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v) {
                ViewPager vg = (ViewPager) getActivity()
                        .findViewById(R.id.id_page_vp);
                vg.setCurrentItem(2, false);
            }
        });


        return appsView;
    }


    @Override
    public void onActivityCreated(Bundle savedInstanceState){
        super.onActivityCreated(savedInstanceState);
    }
}