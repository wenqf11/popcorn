package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
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

import org.json.JSONException;
import org.json.JSONObject;

import java.util.Calendar;

import cn.edu.tsinghua.thss.popcorn.config.Config;


public class RepairActivity extends Activity {
    private JSONObject repairTask = null;
    private int confirmedItem = -1;
    private boolean isConfirmed = false;
    ProgressDialog progressDialog;

    @ViewInject(R.id.repair_report_title)
    private TextView reportTitleTextView;

    @ViewInject(R.id.repair_device_number)
    private TextView deviceNumberTextView;

    @ViewInject(R.id.repair_reporter)
    private TextView reporterTextView;

    @ViewInject(R.id.repair_report_datetime)
    private TextView reportDatetimeTextView;

    @ViewInject(R.id.repair_fault_description)
    private TextView faultDescriptionTextView;

    @ViewInject(R.id.repair_memo)
    private TextView repairMemoTextView;

    @ViewInject(R.id.repair_result)
    private TextView repairResultEditText;

    @ViewInject(R.id.repair_submit)
    private Button repairSubmitButton;

    @OnClick(R.id.repair_submit)
    private void submitRepairButtonClick(View v) {
        if (repairSubmitButton.getText().equals("提交")) {
            submitData();
        }else{
            acceptTask();
        }
    }

    private void acceptTask(){
        String id = "";
        try{
            id = repairTask.getString("id");
        }catch (Exception e){
            e.printStackTrace();
        }

        RequestParams params = new RequestParams();
        params.addBodyParameter("username", Config.DEBUG_USERNAME);
        params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
        params.addBodyParameter("maintain_id", id);
        progressDialog.show();

        HttpUtils http = new HttpUtils();
        http.send(HttpRequest.HttpMethod.POST,
                Config.REPAIR_TASK_CONFIRM_URL,
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
                                Toast.makeText(getApplicationContext(), "成功接受维修任务", Toast.LENGTH_SHORT).show();
                                repairSubmitButton.setText("提交");
                                isConfirmed = true;
                            }
                            else{
                                Toast.makeText(getApplicationContext(), "接受任务失败，请重新提交", Toast.LENGTH_SHORT).show();
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

    private void submitData(){
        String id = "";
        try{
            id = repairTask.getString("id");
        }catch (Exception e){
            e.printStackTrace();
        }
        String note = repairResultEditText.getText().toString();

        RequestParams params = new RequestParams();
        params.addBodyParameter("username", Config.DEBUG_USERNAME);
        params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
        params.addBodyParameter("maintain_id", id);
        params.addBodyParameter("note", note);
        progressDialog.show();

        HttpUtils http = new HttpUtils();
        http.send(HttpRequest.HttpMethod.POST,
                Config.REPAIR_TASK_SUBMIT_URL,
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
        setContentView(R.layout.activity_repair);


        Bundle bundle = this.getIntent().getExtras();
        try {
            repairTask = new JSONObject(bundle.getString("task"));
            confirmedItem = bundle.getInt("position");
        }catch (Exception e) {
        }
        progressDialog = new ProgressDialog(RepairActivity.this, R.style.buffer_dialog);
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
        String creator = "";
        String create_time = "";
        String confirmed = "";
        try{
            title = repairTask.getString("title");
            deviceNumber = repairTask.getString("device_brief");
            faultDescription = repairTask.getString("description");
            creator = repairTask.getString("creator");
            create_time = repairTask.getString("create_time");
            repairMemo = repairTask.getString("memo");
            repairResult = repairTask.getString("note");
            confirmed = repairTask.getString("confirmed");
        }catch (Exception e){
            e.printStackTrace();
        }

        reportTitleTextView.setText(title);
        reporterTextView.setText(creator);
        reportDatetimeTextView.setText(create_time);
        deviceNumberTextView.setText(deviceNumber);
        faultDescriptionTextView.setText(faultDescription);
        repairMemoTextView.setText(repairMemo);
        repairResultEditText.setText(repairResult);
        if(confirmed.equals("true")) {
            repairSubmitButton.setText("提交");
        }else{
            repairSubmitButton.setText("接受任务");
        }
    }

    @Override
    protected  void onDestroy(){
        progressDialog.dismiss();
        super.onDestroy();
    }

    @Override
    public void finish() {
        Bundle bundle = new Bundle();
        bundle.putInt("confirmedItem", confirmedItem);
        bundle.putBoolean("isConfirmed", isConfirmed);
        RepairActivity.this.setResult(RESULT_OK, RepairActivity.this.getIntent().putExtras(bundle));

        super.finish();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.repair, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            RepairActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
