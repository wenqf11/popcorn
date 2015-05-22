package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.content.Context;
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


public class AttendanceActivity extends Activity implements LocationListener,View.OnClickListener{


    private Button mButtonOnWork;
    private Button mButtonOffWork;

    private TextView mTextViewOnWork;
    private TextView mTextViewOffWork;

    private DatePicker datePicker;

    private boolean mStatus = false;
    private String mAddress = "无法定位";

    private LocationManager locationManager;
    private String provider = LocationManager.NETWORK_PROVIDER;
    @Override
    public void onClick(final View v) {
        switch (v.getId()) {
            case R.id.id_btn_attend_on_work:
                mStatus = false;
                getTimeAndLocation();
                findViewById(R.id.id_btn_attend_off_work).setVisibility(View.VISIBLE);
                break;
            case R.id.id_btn_attend_off_work:
                mStatus = true;
                getTimeAndLocation();
                break;
            default:
                break;
        }
        v.setVisibility(View.GONE);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setLayout();

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

        mButtonOnWork  = (Button)findViewById(R.id.id_btn_attend_on_work);
        mButtonOffWork = (Button)findViewById(R.id.id_btn_attend_off_work);
        mTextViewOnWork = (TextView)findViewById(R.id.id_text_attend_on_work);
        mTextViewOffWork = (TextView)findViewById(R.id.id_text_attend_off_work);
        datePicker = (DatePicker)findViewById(R.id.datePicker);

        Calendar calendar=Calendar.getInstance();
        int year=calendar.get(Calendar.YEAR);
        int monthOfYear=calendar.get(Calendar.MONTH);
        int dayOfMonth=calendar.get(Calendar.DAY_OF_MONTH);
        datePicker.init(year, monthOfYear, dayOfMonth, new OnDateChangedListener(){
            @Override
            public void onDateChanged(DatePicker view, int year, int monthOfYear, int dayOfMonth)
            {
            }
        });

        mButtonOnWork.setOnClickListener(this);
        mButtonOffWork.setOnClickListener(this);
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
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm");
            if(mStatus){
                mTextViewOffWork.setText(sdf.format(new Date()) +'\n'+ mAddress);
            }else{
                mTextViewOnWork.setText(sdf.format(new Date()) +'\n'+ mAddress);
            }
            super.onPostExecute(o);
        }
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


