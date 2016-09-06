package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.app.ProgressDialog;
import android.os.Bundle;
import android.view.Gravity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
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

import org.json.JSONException;
import org.json.JSONObject;

import cn.edu.tsinghua.thss.popcorn.config.Config;
import cn.edu.tsinghua.thss.popcorn.utils.PasswordMd5;


public class ChangePasswordActivity extends Activity {
    private static String CHANGE_PASSWORD_URL = Config.LOCAL_IP + "/app/password/";
    ProgressDialog progressDialog;

    @ViewInject(R.id.old_password)
    private TextView oldPasswordEditText;

    @ViewInject(R.id.new_password)
    private TextView newPasswordEditText;

    @ViewInject(R.id.confirm_password)
    private TextView confirmPasswordEditText;

    @OnClick(R.id.submit_passwd_btn)
    private void submitPasswordButtonClick(View v) {
        String oldPassword = oldPasswordEditText.getText().toString();
        String newPassword =newPasswordEditText.getText().toString();
        String confirmPassword =confirmPasswordEditText.getText().toString();
        if(newPasswordEditText.getText().toString().length() < 6 || confirmPasswordEditText.getText().toString().length() < 6){
            Toast.makeText(getApplicationContext(), "密码至少6位", Toast.LENGTH_SHORT).show();
        }
        else if(!newPassword.equals(confirmPassword)){
            Toast.makeText(getApplicationContext(), "两次密码输入不一致", Toast.LENGTH_SHORT).show();
        }
        else {
            progressDialog.show();

            RequestParams params = new RequestParams();
            params.addBodyParameter("username", Config.DEBUG_USERNAME);
            params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
            params.addBodyParameter("password", oldPassword);
            params.addBodyParameter("new_password", newPassword);

            HttpUtils http = new HttpUtils();
            http.send(HttpRequest.HttpMethod.POST,
                    CHANGE_PASSWORD_URL,
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
                                    Toast.makeText(getApplicationContext(), R.string.successfully_changed_password, Toast.LENGTH_SHORT).show();
                                } else {
                                    Toast.makeText(getApplicationContext(), R.string.wrong_old_password, Toast.LENGTH_SHORT).show();
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                            progressDialog.hide();
                        }


                        @Override
                        public void onFailure(HttpException error, String msg) {
                            progressDialog.hide();
                            Toast.makeText(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT).show();
                        }
                    });
        }
    }

    @Override
    protected  void onDestroy(){
        progressDialog.dismiss();
        super.onDestroy();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_change_password);

        ViewUtils.inject(this);

        progressDialog = new ProgressDialog(ChangePasswordActivity.this, R.style.buffer_dialog);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.setMessage("加载中...");
        progressDialog.setIndeterminate(false);
        progressDialog.setCancelable(false);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.change_password, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            ChangePasswordActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
