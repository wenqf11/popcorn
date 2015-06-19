package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.app.Notification;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.res.Resources;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.DatePicker.OnDateChangedListener;
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

import cn.edu.tsinghua.thss.popcorn.config.Config;

public class AttendanceActivity extends Activity implements LocationListener,View.OnClickListener{
    private static String ATTENDANCE_POST_URL = Config.LOCAL_IP + "/app/check/";
    private static String ATTENDANCE_GET_URL = Config.LOCAL_IP + "/app/checkinfo/";

    private boolean mStatus = false;
    private String mAddress = "无法定位";

    private LocationManager locationManager;
    private String provider = LocationManager.NETWORK_PROVIDER;

    ProgressDialog progressDialog;

    @ViewInject(R.id.id_btn_attend_on_work)
    private Button mButtonOnWork;


    @ViewInject(R.id.id_btn_attend_off_work)
    private Button mButtonOffWork;

    @ViewInject(R.id.id_text_attend_on_work)
    private TextView mTextViewOnWork;

    @ViewInject(R.id.id_text_attend_off_work)
    private TextView mTextViewOffWork;

    @ViewInject(R.id.datePicker)
    private DatePicker datePicker;

    @ViewInject(R.id.submit_date)
    private  Button mButtonSubmitDate;

    @OnClick(R.id.submit_date)
    private void submitDateButtonClick(View v) {
        updateAttendanceData();
    }


    @Override
    public void onClick(final View v) {
        switch (v.getId()) {
            case R.id.id_btn_attend_on_work:
                mStatus = false;
                getTimeAndLocation();
                break;
            case R.id.id_btn_attend_off_work:
                mStatus = true;
                getTimeAndLocation();
                break;
            default:
                break;
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setLayout();

        updateAttendanceData();

        locationManager = (LocationManager)getSystemService(Context.LOCATION_SERVICE);
        locationManager.requestLocationUpdates(provider, 0, 0, this);
    }

    //位置发生改变时调用
    @Override
    public void onLocationChanged(Location location) {
    }

    //provider失效时调用
    @Override
    public void onProviderDisabled(String provider) {
    }

    //provider启用时调用
    @Override
    public void onProviderEnabled(String provider) {
    }

    //状态改变时调用
    @Override
    public void onStatusChanged(String provider, int status, Bundle extras) {
    }

    private void setLayout(){
        setContentView(R.layout.activity_attendance);

        progressDialog = new ProgressDialog(AttendanceActivity.this, R.style.buffer_dialog);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.setMessage("数据加载中...");
        progressDialog.setIndeterminate(false);
        progressDialog.setCancelable(false);

        ViewUtils.inject(this);
        Calendar calendar = Calendar.getInstance();
        int year = calendar.get(Calendar.YEAR);
        int monthOfYear = calendar.get(Calendar.MONTH);
        int dayOfMonth = calendar.get(Calendar.DAY_OF_MONTH);
        datePicker.init(year, monthOfYear, dayOfMonth, new OnDateChangedListener(){
            @Override
            public void onDateChanged(DatePicker view, int year, int monthOfYear, int dayOfMonth)
            {
            }
        });
        datePicker.setMaxDate(new Date().getTime());

        mButtonOnWork.setOnClickListener(this);
        mButtonOffWork.setOnClickListener(this);
    }

    private void updateAttendanceData(){
        final int pickedDay = datePicker.getDayOfMonth();
        final int pickedMonth = datePicker.getMonth()+1;
        final int pickedYear = datePicker.getYear();

        String sDay = String.valueOf(pickedDay), sMonth = String.valueOf(pickedMonth);
        if( pickedMonth < 10){
            sMonth = "0" + String.valueOf(pickedMonth);
        }
        if (pickedDay < 10){
            sDay = "0" + String.valueOf(pickedDay);
        }
        String date = String.valueOf(pickedYear) + '-' + sMonth +'-'+ sDay;

        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);
        params.addQueryStringParameter("date", date);

        progressDialog.show();

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(1000 * 10);
        http.send(HttpRequest.HttpMethod.GET,
                ATTENDANCE_GET_URL,
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
                                JSONObject results = jsonObject.getJSONObject("data");
                                String checkIn = results.getString("checkin");
                                String checkOut = results.getString("checkout");
                                mTextViewOnWork.setText(checkIn);
                                mTextViewOffWork.setText(checkOut);
                                mButtonOnWork.setVisibility(View.GONE);
                                mButtonOffWork.setVisibility(View.GONE);
                            }
                            else{
                                mTextViewOnWork.setText("");
                                mTextViewOffWork.setText("");

                                Calendar calendar = Calendar.getInstance();
                                int currentYear = calendar.get(Calendar.YEAR);
                                int currentMonth = calendar.get(Calendar.MONTH)+1;
                                int currentDay = calendar.get(Calendar.DAY_OF_MONTH);
                                if(pickedYear==currentYear && pickedMonth==currentMonth && pickedDay==currentDay) {
                                    mButtonOnWork.setVisibility(View.VISIBLE);
                                    mButtonOffWork.setVisibility(View.GONE);
                                }
                                String msg = jsonObject.getString("data");
                                if(msg.equals("can't connect to database")) {
                                    Toast.makeText(getApplicationContext(), "服务器内部出错", Toast.LENGTH_SHORT).show();
                                }
                            }
                        }catch (JSONException e){
                            e.printStackTrace();
                        }
                        progressDialog.hide();
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getApplicationContext(), error.getExceptionCode() + ":" + msg, Toast.LENGTH_SHORT).show();
                        progressDialog.hide();
                    }
                });
    }

    private void getTimeAndLocation(){
       new getAddrThread().execute();
    }


    public class getAddrThread extends AsyncTask {
        @Override
        protected String doInBackground(Object... params) {

            //通过最后一次的地理位置来获得Location对象
            Location location = locationManager.getLastKnownLocation(provider);
            if (location == null) {
                mAddress = "无法定位";
                return null;
            }


            String latitude = Double.toString(location.getLatitude());
            String longitude = Double.toString(location.getLongitude());
            String url = String.format(
                    "http://maps.google.cn/maps/api/geocode/json?latlng=%s,%s&language=CN",
                    latitude, longitude);

            try {
                URL myURL = new URL(url);
                URLConnection httpsConn =  myURL.openConnection();

                if (httpsConn != null) {
                    InputStreamReader insr = new InputStreamReader(
                            httpsConn.getInputStream(), "UTF-8");
                    BufferedReader br = new BufferedReader(insr);
                    StringBuilder builder = new StringBuilder();

                    for (String s = br.readLine(); s != null; s = br.readLine()) {
                        builder.append(s);
                    }

                    try {
                        JSONObject jsonObject = new JSONObject(builder.toString());
                        JSONArray results = jsonObject.getJSONArray("results");
                        JSONObject component = results.getJSONObject(0);
                        mAddress = component.getString("formatted_address");
                    }catch (JSONException e){
                        e.printStackTrace();
                    }
                    insr.close();
                }
                else{
                    mAddress = "无法定位";
                }
            } catch (IOException e) {
                e.printStackTrace();
                mAddress = "无法定位";
                return null;
            }
            return null;
        }

        @Override
        protected void onPostExecute(Object o) {
            SimpleDateFormat datetimeFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm");
            if(!mStatus){
                if(!mAddress.equals("无法定位")){
                    mButtonOnWork.setVisibility(View.GONE);
                    mTextViewOnWork.setText(datetimeFormat.format(new Date()) +'\n'+ mAddress);
                    mButtonOffWork.setVisibility(View.VISIBLE);
                }else{
                    mStatus = true;
                    Toast.makeText(getApplicationContext(), "无法定位，请检查网络状态是否正常", Toast.LENGTH_SHORT).show();
                }
            }else{
                if(!mAddress.equals("无法定位")){
                    mButtonOffWork.setVisibility(View.GONE);
                    mTextViewOffWork.setText(datetimeFormat.format(new Date()) +'\n'+ mAddress);

                    String start = mTextViewOnWork.getText().toString();
                    String date = start.split(" ")[0];
                    RequestParams params = new RequestParams();
                    params.addBodyParameter("username", "syb1001");
                    params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
                    params.addBodyParameter("date", date);
                    params.addBodyParameter("checkin", mTextViewOnWork.getText().toString());
                    params.addBodyParameter("checkout", mTextViewOffWork.getText().toString());

                    HttpUtils http = new HttpUtils();
                    http.send(HttpRequest.HttpMethod.POST,
                            ATTENDANCE_POST_URL,
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
                                    Toast.makeText(getApplicationContext(), responseInfo.result, Toast.LENGTH_SHORT).show();
                                }

                                @Override
                                public void onFailure(HttpException error, String msg) {
                                    Toast.makeText(getApplicationContext(), error.getExceptionCode() + ":" + msg, Toast.LENGTH_SHORT).show();
                                }
                            });
                }else{
                    Toast.makeText(getApplicationContext(), "无法定位，请检查网络状态是否正常", Toast.LENGTH_SHORT).show();
                }
            }
            super.onPostExecute(o);
        }
    }


    @Override
    protected  void onDestroy(){
        progressDialog.dismiss();
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


