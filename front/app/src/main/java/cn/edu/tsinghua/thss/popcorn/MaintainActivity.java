package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.app.ProgressDialog;
import android.os.Bundle;
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


public class MaintainActivity extends Activity {
    private static String MAINTAIN_TASK_SUBMIT_URL = Config.LOCAL_IP + "/app/maintain/update/";
    private JSONObject maintainTask = null;

    ProgressDialog progressDialog;

    @ViewInject(R.id.maintain_title)
    private TextView maintainTitleTextView;

    @ViewInject(R.id.maintain_device_number)
    private TextView deviceNumberTextView;

    @ViewInject(R.id.maintain_device_name)
    private TextView deviceNameTextView;

    @ViewInject(R.id.maintain_description)
    private TextView maintainDescriptionTextView;

    @ViewInject(R.id.maintain_memo)
    private TextView maintainMemoTextView;

    @ViewInject(R.id.maintain_result)
    private TextView maintainResultEditText;

    @OnClick(R.id.maintain_submit)
    private void submitMaintainButtonClick(View v) {
        String id = "";
        try{
            id = maintainTask.getString("id");
        }catch (Exception e){
        }
        String note = maintainResultEditText.getText().toString();

        RequestParams params = new RequestParams();
        params.addBodyParameter("username", Config.DEBUG_USERNAME);
        params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
        params.addBodyParameter("maintain_id", id);
        params.addBodyParameter("note", note);
        progressDialog.show();

        HttpUtils http = new HttpUtils();
        http.send(HttpRequest.HttpMethod.POST,
                MAINTAIN_TASK_SUBMIT_URL,
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
                                Toast.makeText(getApplicationContext(), "提交成功", Toast.LENGTH_SHORT).show();
                            }
                            else{
                                Toast.makeText(getApplicationContext(), "提交失败，请重新提交", Toast.LENGTH_SHORT).show();
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


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maintain);

        Bundle bundle = this.getIntent().getExtras();
        try {
            maintainTask = new JSONObject(bundle.getString("task"));
        }catch (Exception e) {
        }
        progressDialog = new ProgressDialog(MaintainActivity.this, R.style.buffer_dialog);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.setMessage("数据加载中...");
        progressDialog.setIndeterminate(false);
        progressDialog.setCancelable(false);

        ViewUtils.inject(this);
        setValueOfTextView();
    }

    private void setValueOfTextView(){
        String title = "";
        String deviceNumber = "";
        String faultDescription = "";
        String repairMemo = "";
        String repairResult = "";
        try{
            title = maintainTask.getString("title");
            deviceNumber = maintainTask.getString("device_brief");
            faultDescription = maintainTask.getString("description");
            repairMemo = maintainTask.getString("memo");
            repairResult = maintainTask.getString("note");
        }catch (Exception e){
        }

        maintainTitleTextView.setText(title);
        deviceNumberTextView.setText(deviceNumber);
        maintainDescriptionTextView.setText(faultDescription);
        maintainMemoTextView.setText(repairMemo);
        maintainResultEditText.setText(repairResult);
    }

    @Override
    protected  void onDestroy(){
        progressDialog.dismiss();
        super.onDestroy();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.maintain, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            MaintainActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
