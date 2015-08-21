package cn.edu.tsinghua.thss.popcorn;

import android.app.AlertDialog;
import android.content.Context;
import android.content.SharedPreferences;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.ViewUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;
import com.lidroid.xutils.view.annotation.ViewInject;
import com.lidroid.xutils.view.annotation.event.OnClick;
import com.roomorama.caldroid.CaldroidFragment;
import com.roomorama.caldroid.CaldroidListener;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import com.baidu.location.BDLocation;
import com.baidu.location.BDLocationListener;
import com.baidu.location.LocationClient;
import com.baidu.location.LocationClientOption;
import com.baidu.location.BDNotifyListener;//假如用到位置提醒功能，需要import该类
import com.baidu.location.Poi;

import cn.edu.tsinghua.thss.popcorn.config.Config;

public class AttendanceActivity extends FragmentActivity implements View.OnClickListener{
    public LocationClient mLocationClient = null;
    public BDLocationListener myListener = null;

    CaldroidFragment caldroidFragment;
    Date lastSelected = null;

    @ViewInject(R.id.id_btn_attend_on_work)
    private Button mButtonOnWork;


    @ViewInject(R.id.id_btn_attend_off_work)
    private Button mButtonOffWork;

    @ViewInject(R.id.id_text_attend_on_work)
    private TextView mTextViewOnWork;

    @ViewInject(R.id.id_text_attend_off_work)
    private TextView mTextViewOffWork;

    @Override
    public void onClick(final View v) {
        mLocationClient.start();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setLayout();
        initLocation();
    }

    public class MyLocationListener implements BDLocationListener {
        @Override
        public void onReceiveLocation(BDLocation location) {
            //Receive Location
            StringBuffer sb = new StringBuffer(256);
            sb.append(location.getTime());
            if (location.getLocType() == BDLocation.TypeGpsLocation) {// GPS定位结果
                sb.append("\n"+location.getAddrStr());
            } else if (location.getLocType() == BDLocation.TypeNetWorkLocation) {// 网络定位结果
                sb.append("\n"+location.getAddrStr());
            } else {
                new AlertDialog.Builder(AttendanceActivity.this)
                        .setTitle("网络错误无法定位，请重新定位！")
                        .setPositiveButton("确定", null)
                        .show();
                mLocationClient.stop();
                return;
            }
            if(mButtonOffWork.getVisibility()!=View.VISIBLE) {
                mTextViewOnWork.setText(sb.toString());
                mButtonOffWork.setVisibility(View.VISIBLE);
                mButtonOnWork.setVisibility(View.GONE);
                SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
                String today = dateFormat.format(new Date());
                SharedPreferences sp = getApplicationContext().getSharedPreferences("Attendance", Context.MODE_PRIVATE);
                SharedPreferences.Editor editor = sp.edit();
                editor.putString("checkin", sb.toString());
                editor.putString("date", today);
                editor.apply();
            }else{
                mButtonOffWork.setVisibility(View.GONE);
                mTextViewOffWork.setText(sb.toString());
                submitData();
            }
            mLocationClient.stop();
        }
    }

    private void setLayout(){
        setContentView(R.layout.activity_attendance);
        ViewUtils.inject(this);

        mButtonOnWork.setOnClickListener(this);
        mButtonOffWork.setOnClickListener(this);

        caldroidFragment = new CaldroidFragment();
        Bundle args = new Bundle();
        Calendar cal = Calendar.getInstance();
        args.putInt(CaldroidFragment.MONTH, cal.get(Calendar.MONTH) + 1);
        args.putInt(CaldroidFragment.YEAR, cal.get(Calendar.YEAR));
        caldroidFragment.setArguments(args);

        updateAttendanceData(cal.getTime());

        caldroidFragment.setCaldroidListener(new CaldroidListener() {
            @Override
            public void onSelectDate(Date date, View view) {
                caldroidFragment.setBackgroundResourceForDate(R.color.light_blue, date);
                if (lastSelected != null && lastSelected.compareTo(date) != 0) {
                    caldroidFragment.clearBackgroundResourceForDate(lastSelected);
                }
                lastSelected = date;
                caldroidFragment.refreshView();
                updateAttendanceData(date);
            }
        });

        android.support.v4.app.FragmentTransaction t = getSupportFragmentManager().beginTransaction();
        t.replace(R.id.attendance_calendar, caldroidFragment);
        t.commit();
    }

    private void initLocation(){
        mLocationClient = new LocationClient(getApplicationContext());     //声明LocationClient类
        myListener = new MyLocationListener();
        mLocationClient.registerLocationListener(myListener);    //注册监听函数

        LocationClientOption option = new LocationClientOption();
        option.setLocationMode(LocationClientOption.LocationMode.Hight_Accuracy
        );//可选，默认高精度，设置定位模式，高精度，低功耗，仅设备
        option.setCoorType("bd09ll");//可选，默认gcj02，设置返回的定位结果坐标系
        option.setScanSpan(0);//可选，默认0，即仅定位一次，设置发起定位请求的间隔需要大于等于1000ms才是有效的
        option.setIsNeedAddress(true);//可选，设置是否需要地址信息，默认不需要
        option.setOpenGps(true);//可选，默认false,设置是否使用gps
        option.setLocationNotify(true);//可选，默认false，设置是否当gps有效时按照1S1次频率输出GPS结果
        option.setIgnoreKillProcess(false);//可选，默认false，定位SDK内部是一个SERVICE，并放到了独立进程，设置是否在stop的时候杀死这个进程，默认杀死
        option.SetIgnoreCacheException(false);//可选，默认false，设置是否收集CRASH信息，默认收集
        option.setEnableSimulateGps(false);//可选，默认false，设置是否需要过滤gps仿真结果，默认需要
        mLocationClient.setLocOption(option);
    }

    private void updateAttendanceData(final Date date){
        String date_str = String.format("%tF", date);

        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);
        params.addQueryStringParameter("date", date_str);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.ATTENDANCE_GET_URL,
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
                                JSONObject results = jsonObject.getJSONObject("data");
                                String checkIn = results.getString("checkin");
                                String checkOut = results.getString("checkout");
                                mTextViewOnWork.setText(checkIn);
                                mTextViewOffWork.setText(checkOut);
                                mButtonOnWork.setVisibility(View.GONE);
                                mButtonOffWork.setVisibility(View.GONE);
                            } else {
                                mTextViewOnWork.setText("");
                                mTextViewOffWork.setText("");
                                mButtonOnWork.setVisibility(View.GONE);
                                mButtonOffWork.setVisibility(View.GONE);
                                Calendar now = Calendar.getInstance();
                                Calendar calendar = Calendar.getInstance();
                                calendar.setTime(date);
                                if (calendar.get(Calendar.YEAR) == now.get(Calendar.YEAR)
                                        && now.get(Calendar.DAY_OF_YEAR) == calendar.get(Calendar.DAY_OF_YEAR)) {
                                    mButtonOnWork.setVisibility(View.VISIBLE);
                                    mButtonOffWork.setVisibility(View.GONE);

                                    SharedPreferences sp = getApplicationContext().getSharedPreferences("Attendance", Context.MODE_PRIVATE);
                                    String checkIn = sp.getString("checkin", "");
                                    String date_str = sp.getString("date", "");
                                    SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
                                    String today = dateFormat.format(new Date());
                                    if (!checkIn.equals("") && date_str.equals(today)) {
                                        mTextViewOnWork.setText(checkIn);
                                        mButtonOnWork.setVisibility(View.GONE);
                                        mButtonOffWork.setVisibility(View.VISIBLE);
                                    }
                                }


                                String msg = jsonObject.getString("data");
                                if (msg.equals("can't connect to database")) {
                                    Toast.makeText(getApplicationContext(), "服务器内部出错", Toast.LENGTH_SHORT).show();
                                }
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getApplicationContext(), "网络故障", Toast.LENGTH_SHORT).show();
                    }
                });
    }

    private void submitData(){
        String start = mTextViewOnWork.getText().toString();
        String date = start.split(" ")[0];
        RequestParams params = new RequestParams();
        params.addBodyParameter("username", Config.DEBUG_USERNAME);
        params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
        params.addBodyParameter("date", date);
        params.addBodyParameter("checkin", mTextViewOnWork.getText().toString());
        params.addBodyParameter("checkout", mTextViewOffWork.getText().toString());

        HttpUtils http = new HttpUtils();
        http.send(HttpRequest.HttpMethod.POST,
                Config.ATTENDANCE_POST_URL,
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
                        SharedPreferences sp = getApplicationContext().getSharedPreferences("Attendance", Context.MODE_PRIVATE);
                        SharedPreferences.Editor editor = sp.edit();
                        editor.putString("checkin", "");
                        editor.apply();
                        Toast.makeText(getApplicationContext(), "今日打卡成功", Toast.LENGTH_SHORT).show();
                    }

                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getApplicationContext(), "网络错误数据提交失败，请重新提交", Toast.LENGTH_SHORT).show();
                    }
                });
    }

    @Override
    protected  void onDestroy(){
        mLocationClient.stop();
        super.onDestroy();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.attendance, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            AttendanceActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}


