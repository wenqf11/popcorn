package cn.edu.tsinghua.thss.popcorn;

import java.util.ArrayList;
import java.util.List;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.SharedPreferences;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.os.Handler;
import android.os.Message;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.view.ViewPager;
import android.support.v4.view.ViewPager.OnPageChangeListener;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.KeyEvent;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.beardedhen.androidbootstrap.FontAwesomeText;
import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import cn.edu.tsinghua.thss.popcorn.QRcode.QRcodeActivity;
import cn.edu.tsinghua.thss.popcorn.config.Config;
import cn.edu.tsinghua.thss.popcorn.ui.AppsFragment;
import cn.edu.tsinghua.thss.popcorn.ui.FragmentAdapter;
import cn.edu.tsinghua.thss.popcorn.ui.MineFragment;
import cn.edu.tsinghua.thss.popcorn.ui.RecordFragment;
import cn.edu.tsinghua.thss.popcorn.ui.ReportFragment;
import cn.edu.tsinghua.thss.popcorn.update.UpdateInfoParser;

/**
 * @author wenqingfu
 * @date 2015.04.12
 * @email thssvince@163.com
 */

public class MainActivity extends FragmentActivity {
    private static int UPDATE_UNDO = 1, UPDATE_VERSION = 2;
	private ViewPager mPageVp;
    private String localVersion = "", remoteVersion = "";
	private List<Fragment> mFragmentList = new ArrayList<Fragment>();
	private FragmentAdapter mFragmentAdapter;

	private TextView mTabRecordTv, mTabRepairTv, mTabAppsTv, mTabMineTv,mBodyMeterTv,mBodyRepairTv,
            mBodyMaintainTv,mbottomTabMeterTv, mbottomTabAppTv, mbottomTabMineTv, mBodyTaskTv;

    private FontAwesomeText mTabRecordFat, mTabRepairFat, mTabAppsFat, mTabMineFat;

    private View mTabRecordLayout, mTabRepairLayout, mTabAppsLayout, mTabMineLayout;
	/**
	 * Tab的那个引导线
	 */
	private ImageView mTabLineIv;

	/**
	 * ViewPager的当前选中页
	 */
	private int currentIndex;

	/**
	 * 屏幕的宽度
	 */
	private int screenWidth;

    /**
     * tab 的数量
     */
    private int numOfTabs = 4;

    /**
     * 未完成的任务数量
     */
    private int mRecordUnfinished = 0;
    private int mRepairUnfinished = 0;
    private int mMaintainUnfinished = 0;
    private int mTaskUnfinished = 0;
    private boolean isUnRecordCallbackFinished = false;
    private boolean isUnRepairCallbackFinished = false;
    private boolean isUnMaintainCallbackFinished = false;
    private boolean isUnTaskCallbackFinished = false;
    private boolean alarmRing = false;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
		findById();
		init();
		initTabLineWidth();
        setLocalUsername();
        newTaskHandler.postDelayed(runnable, Config.MAIN_UPDATE_INTERVAL);
        initCacheData();
	}

    private void initCacheData(){
        SharedPreferences sp = getApplicationContext().getSharedPreferences("recordData", MODE_PRIVATE);
        SharedPreferences.Editor editor = sp.edit();
        editor.clear();
        editor.apply();

        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.GET_BONUS_TIME_URL,
                params,
                new RequestCallBack<String>() {
                    @Override
                    public void onStart() {
                    }

                    @Override
                    public void onLoading(long total, long current, boolean isUploading) {
                    }

                    @Override
                    public void onSuccess(ResponseInfo<String> responseInfo) {
                        try {
                            JSONObject jsonObject = new JSONObject(responseInfo.result);
                            String status = jsonObject.getString("status");

                            if (status.equals("ok")) {
                                JSONObject bonusInfo = jsonObject.getJSONObject("data");
                                String start_time = bonusInfo.getString("start_time");
                                String end_time = bonusInfo.getString("end_time");
                                SharedPreferences sp = getApplicationContext().getSharedPreferences("BonusData", MODE_PRIVATE);
                                SharedPreferences.Editor editor = sp.edit();
                                editor.putString("start_time", start_time);
                                editor.putString("end_time", end_time);
                                editor.apply();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }

                    @Override
                    public void onFailure(HttpException error, String msg) {
                    }
                });
    }

    @Override
    protected void onStart() {
        super.onStart();
        checkVersionUpdate();
    }

    public String getVersionName() throws Exception {
        //getPackageName()是你当前类的包名，0代表是获取版本信息
        PackageManager packageManager = getPackageManager();
        PackageInfo packInfo = packageManager.getPackageInfo(getPackageName(),
                0);
        return packInfo.versionName;
    }

    private void checkVersionUpdate(){
        try {
            localVersion = getVersionName();
        }catch (Exception e) {
            e.printStackTrace();
        }

        new Thread(){
            @Override
            public void run() {
                // TODO Auto-generated method stub
                super.run();
                remoteVersion = UpdateInfoParser.getRemoteVersion();
                Message message = new Message();
                message.what = UPDATE_VERSION;
                handler.sendMessage(message);
            }
        }.start();
    }

    private void setLocalUsername(){
        SharedPreferences sp = getApplicationContext().getSharedPreferences("userInfo", Context.MODE_PRIVATE);
        Config.DEBUG_USERNAME = sp.getString("USERNAME", "");
        Config.ACCESS_TOKEN = sp.getString("ACCESS_TOKEN", "");
    }

    Handler handler = new Handler() {
        public void handleMessage(Message msg) {
            if (msg.what == UPDATE_UNDO) {
                alarmRing = false;
                isUnRepairCallbackFinished = false;
                isUnRecordCallbackFinished = false;
                isUnMaintainCallbackFinished = false;
                isUnTaskCallbackFinished = false;
                getUnRepairNum();
                getUnMaintainNum();
                getUnRecordNum();
                getUnTaskNum();
            }else if (msg.what == UPDATE_VERSION){
                if(remoteVersion.equals("") || remoteVersion.equals(localVersion)){
                    mbottomTabMineTv.setVisibility(View.GONE);
                }else{
                    mbottomTabMineTv.setVisibility(View.VISIBLE);
                }
            }
            super.handleMessage(msg);
        };
    };

	private void findById() {
		mTabRecordTv = (TextView) this.findViewById(R.id.id_record_tv);
        mTabRepairTv = (TextView) this.findViewById(R.id.id_repair_tv);
        mTabAppsTv = (TextView) this.findViewById(R.id.id_apps_tv);
        mTabMineTv = (TextView) this.findViewById(R.id.id_mine_tv);

        mTabRecordFat = (FontAwesomeText) findViewById(R.id.id_record_fat);
        mTabRepairFat = (FontAwesomeText) findViewById(R.id.id_repair_fat);
        mTabAppsFat = (FontAwesomeText) findViewById(R.id.id_apps_fat);
        mTabMineFat = (FontAwesomeText) findViewById(R.id.id_mine_fat);

        mTabRecordLayout = this.findViewById(R.id.id_tab_record_ll);
        mTabRepairLayout = this.findViewById(R.id.id_tab_repair_ll);
        mTabAppsLayout = this.findViewById(R.id.id_tab_apps_ll);
        mTabMineLayout = this.findViewById(R.id.id_tab_mine_ll);

        mbottomTabMeterTv = (TextView)this.findViewById(R.id.main_bottom_tab_meter_id);
        mbottomTabMineTv = (TextView)this.findViewById(R.id.main_bottom_tab_mine_id);
        mbottomTabAppTv = (TextView)this.findViewById(R.id.main_bottom_tab_app_id);
        mBodyMeterTv = (TextView)this.findViewById(R.id.main_body_app_meter_id);
        mBodyRepairTv = (TextView)this.findViewById(R.id.main_body_app_repair_id);
        mBodyMaintainTv = (TextView)this.findViewById(R.id.main_body_app_maintain_id);
        mBodyTaskTv = (TextView)this.findViewById(R.id.main_body_app_task_id);

		mTabLineIv = (ImageView) this.findViewById(R.id.id_tab_line_iv);
		mPageVp = (ViewPager) this.findViewById(R.id.id_page_vp);
	}

	private void init() {
        AppsFragment mAppsFg = new AppsFragment();
        RecordFragment mRecordFg = new RecordFragment();
        ReportFragment mReportFg = new ReportFragment();
        MineFragment mMineFg = new MineFragment();

        mFragmentList.add(mAppsFg);
		mFragmentList.add(mRecordFg);
		mFragmentList.add(mReportFg);
        mFragmentList.add(mMineFg);
        if (mFragmentAdapter == null) {
            mFragmentAdapter = new FragmentAdapter(this.getSupportFragmentManager(), mFragmentList);
        } else {
            mFragmentAdapter.setFragmentsList(getSupportFragmentManager(),mFragmentList);
        }
		mPageVp.setAdapter(mFragmentAdapter);
		mPageVp.setCurrentItem(0);

        mTabAppsLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                mPageVp.setCurrentItem(0, false);
            }
        });

        mTabRecordLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                mPageVp.setCurrentItem(1, false);
            }
        });

        mTabRepairLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                mPageVp.setCurrentItem(2, false);
            }
        });

        mTabMineLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                mPageVp.setCurrentItem(3, false);
            }
        });

		mPageVp.setOnPageChangeListener(new OnPageChangeListener() {

            /**
             * state滑动中的状态 有三种状态（0，1，2） 1：正在滑动 2：滑动完毕 0：什么都没做。
             */
            @Override
            public void onPageScrollStateChanged(int state) {
                // code goes here
            }

            /**
             * position :当前页面，及你点击滑动的页面 offset:当前页面偏移的百分比
             * offsetPixels:当前页面偏移的像素位置
             * This method will be invoked when the current page is scrolled
             */
            @Override
            public void onPageScrolled(int position, float offset,
                                       int offsetPixels) {
                LinearLayout.LayoutParams lp = (LinearLayout.LayoutParams) mTabLineIv
                        .getLayoutParams();

                //Log.e("offset:", offset + "");
                /**
                 * 利用currentIndex(当前所在页面)和position(下一个页面)以及offset来
                 * 设置mTabLineIv的左边距 滑动场景：
                 * 记4个页面,
                 * 从左到右分别为0,1,2, 3
                 */

                if (currentIndex == 0 && position == 0)// 0->1
                {
                    lp.leftMargin = (int) (offset * (screenWidth * 1.0 / numOfTabs) + currentIndex
                            * (screenWidth / numOfTabs));

                } else if (currentIndex == 1 && position == 0) // 1->0
                {
                    lp.leftMargin = (int) (-(1 - offset)
                            * (screenWidth * 1.0 / numOfTabs) + currentIndex
                            * (screenWidth / numOfTabs));

                } else if (currentIndex == 1 && position == 1) // 1->2
                {
                    lp.leftMargin = (int) (offset * (screenWidth * 1.0 / numOfTabs) + currentIndex
                            * (screenWidth / numOfTabs));
                } else if (currentIndex == 2 && position == 1) // 2->1
                {
                    lp.leftMargin = (int) (-(1 - offset)
                            * (screenWidth * 1.0 / numOfTabs) + currentIndex
                            * (screenWidth / numOfTabs));
                } else if (currentIndex == 2 && position == 2) // 2->3
                {
                    lp.leftMargin = (int) (offset * (screenWidth * 1.0 / numOfTabs) + currentIndex
                            * (screenWidth / numOfTabs));
                } else if (currentIndex == 3 && position == 2) // 3->2
                {
                    lp.leftMargin = (int) (-(1 - offset)
                            * (screenWidth * 1.0 / numOfTabs) + currentIndex
                            * (screenWidth / numOfTabs));
                } else if (currentIndex == 3 && position == 3) // 3->3
                {
                    lp.leftMargin = (int) (offset * (screenWidth * 1.0 / numOfTabs) + currentIndex
                            * (screenWidth / numOfTabs));
                }
                mTabLineIv.setLayoutParams(lp);
            }


            // This method will be invoked when a new page becomes selected.
            @Override
            public void onPageSelected(int position) {
                resetTabColor();
                switch (position) {
                    case 0:
                        mTabAppsTv.setTextColor(Color.parseColor("#33B5E5"));
                        mTabAppsFat.setTextColor(Color.parseColor("#33B5E5"));
                        break;
                    case 1:

                        mTabRecordTv.setTextColor(Color.parseColor("#33B5E5"));
                        mTabRecordFat.setTextColor(Color.parseColor("#33B5E5"));
                        break;
                    case 2:
                        mTabRepairTv.setTextColor(Color.parseColor("#33B5E5"));
                        mTabRepairFat.setTextColor(Color.parseColor("#33B5E5"));
                        break;
                    case 3:
                        mTabMineTv.setTextColor(Color.parseColor("#33B5E5"));
                        mTabMineFat.setTextColor(Color.parseColor("#33B5E5"));
                        break;
                }
                currentIndex = position;
            }
        });

	}


    private void updateHint(){
        Message message = new Message();
        message.what = UPDATE_UNDO;
        handler.sendMessage(message);
    }
	/**
	 * 设置滑动条的宽度为屏幕的1/4(根据Tab的个数而定)
	 */
	private void initTabLineWidth() {
		DisplayMetrics dpMetrics = new DisplayMetrics();
		getWindow().getWindowManager().getDefaultDisplay()
				.getMetrics(dpMetrics);
		screenWidth = dpMetrics.widthPixels;
		LinearLayout.LayoutParams lp = (LinearLayout.LayoutParams) mTabLineIv
				.getLayoutParams();
		lp.width = screenWidth / numOfTabs;
		mTabLineIv.setLayoutParams(lp);
	}

	/**
	 * 重置导航栏的颜色
	 */
	private void resetTabColor() {
		mTabRecordTv.setTextColor(Color.parseColor("#D3D3D3"));
		mTabRepairTv.setTextColor(Color.parseColor("#D3D3D3"));
        mTabAppsTv.setTextColor(Color.parseColor("#D3D3D3"));
        mTabMineTv.setTextColor(Color.parseColor("#D3D3D3"));

        mTabRecordFat.setTextColor(Color.parseColor("#D3D3D3"));
        mTabRepairFat.setTextColor(Color.parseColor("#D3D3D3"));
        mTabAppsFat.setTextColor(Color.parseColor("#D3D3D3"));
        mTabMineFat.setTextColor(Color.parseColor("#D3D3D3"));
	}

    public void startAlarmPush() {
        Intent intent = new Intent(MainActivity.this, AlarmReceiver.class);
        PendingIntent sender = PendingIntent.getBroadcast(MainActivity.this, 0, intent, 0);

        AlarmManager am=(AlarmManager)getSystemService(ALARM_SERVICE);
        am.set(AlarmManager.RTC_WAKEUP, System.currentTimeMillis(), sender);
    }


    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK && event.getRepeatCount() == 0) {
            Intent intent = new Intent(Intent.ACTION_MAIN);
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            intent.addCategory(Intent.CATEGORY_HOME);
            this.startActivity(intent);
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        switch (item.getItemId()){
            case R.id.scan_btn:
                try {
                    Intent intent = new Intent(this, QRcodeActivity.class);
                    Bundle bundle = new Bundle();
                    intent.putExtras(bundle);
                    startActivity(intent);
                }
                catch (Exception e){
                    Log.e("Exception", e.getMessage(), e);
                }
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }

    private void getUnRepairNum(){
        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.REPAIR_TASK_LIST_URL,
                params,
                new RequestCallBack<String>() {
                    @Override
                    public void onStart() {
                    }

                    @Override
                    public void onLoading(long total, long current, boolean isUploading) {
                    }

                    @Override
                    public void onSuccess(ResponseInfo<String> responseInfo) {
                        try{
                            JSONObject jsonObject = new JSONObject(responseInfo.result);
                            String status = jsonObject.getString("status");
                            if(status.equals("ok")) {
                                JSONArray repairTaskList = jsonObject.getJSONArray("data");
                                mRepairUnfinished = repairTaskList.length();
                            }
                            else{
                                Toast.makeText(getApplicationContext(), "服务器内部错误", Toast.LENGTH_SHORT).show();
                            }
                        }catch (JSONException e){
                            e.printStackTrace();
                        }


                        if (mRepairUnfinished > 0) {
                            if(mBodyRepairTv == null) {
                                mBodyRepairTv = (TextView)findViewById(R.id.main_body_app_repair_id);
                            }
                            if(mRepairUnfinished > Integer.parseInt(mBodyRepairTv.getText().toString())){
                                alarmRing = true;
                            }
                            mBodyRepairTv.setText(String.valueOf(mRepairUnfinished));
                            mBodyRepairTv.setVisibility(View.VISIBLE);
                        }
                        else {
                            if(mBodyRepairTv == null) {
                                mBodyRepairTv = (TextView)findViewById(R.id.main_body_app_repair_id);
                            }
                            mBodyRepairTv.setVisibility(View.GONE);
                        }

                        isUnRepairCallbackFinished = true;

                        if(isUnRepairCallbackFinished&&isUnRecordCallbackFinished&&isUnMaintainCallbackFinished&&isUnTaskCallbackFinished){
                            if(mRecordUnfinished + mRepairUnfinished + mMaintainUnfinished + mTaskUnfinished + mTaskUnfinished > 0) {
                                mbottomTabAppTv.setText(String.valueOf(mRecordUnfinished + mRepairUnfinished + mMaintainUnfinished + mTaskUnfinished));
                                mbottomTabAppTv.setVisibility(View.VISIBLE);
                            }else{
                                mbottomTabAppTv.setVisibility(View.GONE);
                            }

                            if(alarmRing){
                                startAlarmPush();
                            }
                        }
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getApplicationContext(), "网络故障", Toast.LENGTH_SHORT).show();
                        isUnRepairCallbackFinished = true;
                    }
                });
    }

    private void getUnMaintainNum(){
        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.MAINTAIN_TASK_LIST_URL,
                params,
                new RequestCallBack<String>() {
                    @Override
                    public void onStart() {
                    }
                    @Override
                    public void onLoading(long total, long current, boolean isUploading) {
                    }
                    @Override
                    public void onSuccess(ResponseInfo<String> responseInfo) {
                        try {
                            JSONObject jsonObject = new JSONObject(responseInfo.result);
                            String status = jsonObject.getString("status");
                            if (status.equals("ok")) {
                                JSONArray maintainTaskList = jsonObject.getJSONArray("data");
                                mMaintainUnfinished = maintainTaskList.length();
                            } else {
                                Toast.makeText(getApplicationContext(), "服务器内部错误", Toast.LENGTH_SHORT).show();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                        if(mMaintainUnfinished > 0) {
                            if(mBodyMaintainTv == null) {
                                mBodyMaintainTv = (TextView)findViewById(R.id.main_body_app_maintain_id);
                            }
                            if(mMaintainUnfinished > Integer.parseInt(mBodyMaintainTv.getText().toString())){
                                alarmRing = true;
                            }
                            mBodyMaintainTv.setText(String.valueOf(mMaintainUnfinished));
                            mBodyMaintainTv.setVisibility(View.VISIBLE);
                        }
                        else {
                            if(mBodyMaintainTv == null) {
                                mBodyMaintainTv = (TextView)findViewById(R.id.main_body_app_maintain_id);
                            }
                            mBodyMaintainTv.setVisibility(View.GONE);
                        }

                        isUnRecordCallbackFinished = true;

                        if(isUnRepairCallbackFinished&&isUnRecordCallbackFinished&&isUnMaintainCallbackFinished&&isUnTaskCallbackFinished){
                            if(mRecordUnfinished + mRepairUnfinished + mMaintainUnfinished + mTaskUnfinished + mTaskUnfinished > 0) {
                                mbottomTabAppTv.setText(String.valueOf(mRecordUnfinished + mRepairUnfinished + mMaintainUnfinished + mTaskUnfinished));
                                mbottomTabAppTv.setVisibility(View.VISIBLE);
                            }else{
                                mbottomTabAppTv.setVisibility(View.GONE);
                            }

                            if(alarmRing){
                                startAlarmPush();
                            }
                        }
                    }
                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getApplicationContext(), "网络故障", Toast.LENGTH_SHORT).show();
                        isUnRecordCallbackFinished = true;
                    }
                });
    }


    private void getUnRecordNum(){
        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.ROUTE_GET_URL,
                params,
                new RequestCallBack<String>() {

                    @Override
                    public void onStart() {
                    }

                    @Override
                    public void onLoading(long total, long current, boolean isUploading) {
                    }

                    @Override
                    public void onSuccess(ResponseInfo<String> responseInfo) {
                        try {
                            JSONObject jsonObject = new JSONObject(responseInfo.result);
                            String status = jsonObject.getString("status");
                            if (status.equals("ok")) {
                                JSONArray results = jsonObject.getJSONArray("data");
                                mRecordUnfinished = results.length();
                            }else{
                                Toast.makeText(getApplicationContext(), "服务器内部错误", Toast.LENGTH_SHORT).show();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                        if (mRecordUnfinished > 0) {
                            mbottomTabMeterTv.setText(String.valueOf(mRecordUnfinished));
                            mbottomTabMeterTv.setVisibility(View.VISIBLE);
                            if(mBodyMeterTv == null) {
                                mBodyMeterTv = (TextView)findViewById(R.id.main_body_app_meter_id);
                            }
                            if(mRecordUnfinished > Integer.parseInt(mBodyMeterTv.getText().toString())){
                                alarmRing = true;
                            }
                            mBodyMeterTv.setText(String.valueOf(mRecordUnfinished));
                            mBodyMeterTv.setVisibility(View.VISIBLE);
                        }
                        else {
                            if(mBodyMeterTv == null) {
                                mBodyMeterTv = (TextView)findViewById(R.id.main_body_app_meter_id);
                            }
                            mbottomTabMeterTv.setVisibility(View.GONE);
                        }

                        isUnMaintainCallbackFinished = true;

                        if(isUnRepairCallbackFinished&&isUnRecordCallbackFinished&&isUnMaintainCallbackFinished&&isUnTaskCallbackFinished){
                            if(mRecordUnfinished + mRepairUnfinished + mMaintainUnfinished + mTaskUnfinished + mTaskUnfinished > 0) {
                                mbottomTabAppTv.setText(String.valueOf(mRecordUnfinished + mRepairUnfinished + mMaintainUnfinished + mTaskUnfinished));
                                mbottomTabAppTv.setVisibility(View.VISIBLE);
                            }else{
                                mbottomTabAppTv.setVisibility(View.GONE);
                            }

                            if(alarmRing){
                                startAlarmPush();
                            }
                        }
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getApplicationContext(), "网络故障", Toast.LENGTH_SHORT).show();
                        isUnMaintainCallbackFinished = true;
                    }
                });
    }


    private void getUnTaskNum(){
        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.TASK_LIST_URL,
                params,
                new RequestCallBack<String>() {
                    @Override
                    public void onStart() {
                    }
                    @Override
                    public void onLoading(long total, long current, boolean isUploading) {
                    }
                    @Override
                    public void onSuccess(ResponseInfo<String> responseInfo) {
                        try {
                            JSONObject jsonObject = new JSONObject(responseInfo.result);
                            String status = jsonObject.getString("status");
                            if (status.equals("ok")) {
                                JSONArray taskList = jsonObject.getJSONArray("data");
                                mTaskUnfinished = taskList.length();
                            } else {
                                Toast.makeText(getApplicationContext(), "服务器内部错误", Toast.LENGTH_SHORT).show();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                        if(mTaskUnfinished > 0) {
                            if(mBodyTaskTv == null) {
                                mBodyTaskTv = (TextView)findViewById(R.id.main_body_app_task_id);
                            }
                            if(mTaskUnfinished > Integer.parseInt(mBodyTaskTv.getText().toString())){
                                alarmRing = true;
                            }
                            mBodyTaskTv.setText(String.valueOf(mTaskUnfinished));
                            mBodyTaskTv.setVisibility(View.VISIBLE);
                        }
                        else {
                            if(mBodyTaskTv == null) {
                                mBodyTaskTv = (TextView)findViewById(R.id.main_body_app_task_id);
                            }
                            mBodyTaskTv.setVisibility(View.GONE);
                        }

                        isUnTaskCallbackFinished = true;

                        if(isUnRepairCallbackFinished&&isUnRecordCallbackFinished&&isUnMaintainCallbackFinished&&isUnTaskCallbackFinished){
                            if(mRecordUnfinished + mRepairUnfinished + mMaintainUnfinished + mTaskUnfinished + mTaskUnfinished > 0) {
                                mbottomTabAppTv.setText(String.valueOf(mRecordUnfinished + mRepairUnfinished + mMaintainUnfinished + mTaskUnfinished));
                                mbottomTabAppTv.setVisibility(View.VISIBLE);
                            }else{
                                mbottomTabAppTv.setVisibility(View.GONE);
                            }

                            if(alarmRing){
                                startAlarmPush();
                            }
                        }
                    }
                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getApplicationContext(), "网络故障", Toast.LENGTH_SHORT).show();
                        isUnTaskCallbackFinished = true;
                    }
                });
    }
    @Override
    public void onDestroy(){
        newTaskHandler.removeCallbacks(runnable);
        super.onDestroy();
    }


    Handler newTaskHandler = new Handler();
    Runnable runnable=new Runnable() {
        @Override
        public void run() {
            updateHint();
            newTaskHandler.postDelayed(this, Config.MAIN_UPDATE_INTERVAL);
        }
    };
}
