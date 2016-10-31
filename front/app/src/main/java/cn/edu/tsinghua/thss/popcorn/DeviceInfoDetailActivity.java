package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
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

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import cn.edu.tsinghua.thss.popcorn.config.Config;
import cn.edu.tsinghua.thss.popcorn.utils.NoRepeatToast;


public class DeviceInfoDetailActivity extends Activity {
    private String brief;
    private String name;
    private String producer;
    private String type;
    private String serial;
    private String brand;
    private String model;
    private String bought_time;
    private String location;
    private String memo;

    @ViewInject(R.id.device_info_brief)
    private TextView deviceInfoBrief;

    @ViewInject(R.id.device_info_name)
    private TextView deviceInfoName;

    @ViewInject(R.id.device_info_producer)
    private TextView deviceInfoProducer;

    @ViewInject(R.id.device_info_type)
    private TextView deviceInfoType;

    @ViewInject(R.id.device_info_serial)
    private TextView deviceInfoSerial;

    @ViewInject(R.id.device_info_brand)
    private TextView deviceInfoBrand;

    @ViewInject(R.id.device_info_model)
    private TextView deviceInfoModel;

    @ViewInject(R.id.device_info_bought_time)
    private TextView deviceInfoBoughtTime;

    @ViewInject(R.id.device_info_location)
    private TextView deviceInfoLocation;

    @ViewInject(R.id.device_info_memo)
    private TextView deviceInfoMemo;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_device_info_detail);
        ViewUtils.inject(this);

        getDeviceInfo();
    }

    private void getDeviceInfo(){
        Bundle tmp_bundle = this.getIntent().getExtras();
        String deviceBrief = tmp_bundle.getString("device_brief");
        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);
        params.addQueryStringParameter("device_brief", deviceBrief);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.GET_DEVICE_INFO_URL,
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
                                JSONObject deviceInfo = jsonObject.getJSONObject("data");
                                brief = deviceInfo.getString("brief");
                                name = deviceInfo.getString("name");
                                producer = deviceInfo.getString("producer");
                                type = deviceInfo.getString("type");
                                serial = deviceInfo.getString("serial");
                                brand = deviceInfo.getString("brand");
                                model = deviceInfo.getString("model");
                                bought_time = deviceInfo.getString("bought_time");
                                location = deviceInfo.getString("location");
                                memo = deviceInfo.getString("memo");

                                setDeviceInfoView();
                            }else{
                                Toast.makeText(getApplicationContext(), "网络连接异常或者设备不存在", Toast.LENGTH_SHORT).show();
                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        //Toast.makeText(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT).show();
                        NoRepeatToast.showToast(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT);
                    }
                });
    }

    private  void setDeviceInfoView(){
        deviceInfoBrief.setText(brief);
        deviceInfoName.setText(name);
        deviceInfoProducer.setText(producer);
        deviceInfoType.setText(type);
        deviceInfoSerial.setText(serial);
        deviceInfoBrand.setText(brand);
        deviceInfoModel.setText(model);
        deviceInfoBoughtTime.setText(bought_time);
        deviceInfoLocation.setText(location);
        deviceInfoMemo.setText(memo);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.device_info_detail, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            DeviceInfoDetailActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
