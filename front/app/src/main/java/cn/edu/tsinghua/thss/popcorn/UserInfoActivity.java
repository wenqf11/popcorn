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

import org.json.JSONException;
import org.json.JSONObject;

import cn.edu.tsinghua.thss.popcorn.config.Config;


public class UserInfoActivity extends Activity {
    private String name;
    private String department;
    private String gender;
    private String mobile;
    private String email;
    private String address;
    private String birthday;

    @ViewInject(R.id.user_info_name)
    private TextView userInfoName;

    @ViewInject(R.id.user_info_department)
    private TextView userInfoDepartment;

    @ViewInject(R.id.user_info_gender)
    private TextView userInfoGender;

    @ViewInject(R.id.user_info_mobile)
    private TextView userInfoMobile;

    @ViewInject(R.id.user_info_email)
    private TextView userInfoEmail;

    @ViewInject(R.id.user_info_address)
    private TextView userInfoAddress;

    @ViewInject(R.id.user_info_birthday)
    private TextView userInfoBirthday;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_info);
        ViewUtils.inject(this);
        getUserInfo();
    }

    private void getUserInfo(){
        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.GET_USER_INFO_URL,
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
                                JSONObject userInfo = jsonObject.getJSONObject("data");
                                name = userInfo.getString("name");
                                gender = userInfo.getString("gender");
                                if(gender.equals("1")){
                                    gender="男";
                                }
                                birthday = userInfo.getString("birthday");
                                mobile = userInfo.getString("mobile");
                                email = userInfo.getString("email");
                                department = userInfo.getString("department");
                                address = userInfo.getString("address");
                                setUserInfoView();
                            } else {
                                Toast.makeText(getApplicationContext(), "网络连接出错", Toast.LENGTH_SHORT).show();
                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getApplicationContext(), error.getExceptionCode() + ":" + msg, Toast.LENGTH_SHORT).show();
                    }
                });
    }

    private  void setUserInfoView(){
        userInfoName.setText(name);
        userInfoGender.setText(gender);
        userInfoBirthday.setText(birthday);
        userInfoMobile.setText(mobile);
        userInfoEmail.setText(email);
        userInfoDepartment.setText(department);
        userInfoAddress.setText(address);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_user_info, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.close_btn) {
            this.finish();
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
