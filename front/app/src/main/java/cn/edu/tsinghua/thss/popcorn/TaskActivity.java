package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
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

import cn.edu.tsinghua.thss.popcorn.config.Config;
import cn.edu.tsinghua.thss.popcorn.utils.NoRepeatToast;


public class TaskActivity extends Activity {
    private JSONObject taskObj = null;

    private int position = -1;
    private boolean isConfirmed = false;
    private boolean isUpdated = false;
    private boolean isSubmitted = false;
    private String updatedNote = "";

    ProgressDialog progressDialog;

    @ViewInject(R.id.task_title)
    private TextView taskTitleTextView;

    @ViewInject(R.id.task_description)
    private TextView taskDescriptionTextView;

    @ViewInject(R.id.task_memo)
    private TextView taskMemoTextView;

    @ViewInject(R.id.task_result)
    private TextView taskResultEditText;

    @ViewInject(R.id.task_submit)
    private Button taskSubmitButton;

    @ViewInject(R.id.task_update)
    private Button taskUpdateButton;

    @OnClick(R.id.task_update)
    private void updateTaskButtonClick(View v){
        String id = "";
        try{
            id = taskObj.getString("id");
        }catch (Exception e){
            e.printStackTrace();
        }
        String note = taskResultEditText.getText().toString();
        updatedNote = note;

        RequestParams params = new RequestParams();
        params.addBodyParameter("username", Config.DEBUG_USERNAME);
        params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
        params.addBodyParameter("task_id", id);
        params.addBodyParameter("note", note);
        //progressDialog.show();

        HttpUtils http = new HttpUtils();
        http.send(HttpRequest.HttpMethod.POST,
                Config.TASK_UPDATE_URL,
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
                                Toast.makeText(getApplicationContext(), "暂存成功", Toast.LENGTH_SHORT).show();
                                isUpdated = true;
                            }
                            else{
                                Toast.makeText(getApplicationContext(), "暂存失败，请重新提交", Toast.LENGTH_SHORT).show();
                            }
                        }catch (JSONException e){
                            e.printStackTrace();
                        }
                        //progressDialog.hide();
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        //Toast.makeText(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT).show();
                        NoRepeatToast.showToast(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT);
                        //progressDialog.hide();
                    }
                });
    }

    @OnClick(R.id.task_submit)
    private void submitTaskButtonClick(View v) {
        if (taskSubmitButton.getText().equals("提交")) {
            new AlertDialog.Builder(TaskActivity.this)
                    .setTitle("提示")
                    .setMessage("提交后内容将无法修改，是否确定提交？")
                    .setNegativeButton("确定",
                            new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialoginterface, int i) {
                                    submitData();
                                }
                            }).setPositiveButton("取消", null).show();
        }else{
            acceptTask();
        }
    }

    private void acceptTask(){
        String id = "";
        try{
            id = taskObj.getString("id");
        }catch (Exception e){
            e.printStackTrace();
        }

        RequestParams params = new RequestParams();
        params.addBodyParameter("username", Config.DEBUG_USERNAME);
        params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
        params.addBodyParameter("task_id", id);
        //progressDialog.show();

        HttpUtils http = new HttpUtils();
        http.send(HttpRequest.HttpMethod.POST,
                Config.TASK_CONFIRM_URL,
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
                                Toast.makeText(getApplicationContext(), "成功接受任务", Toast.LENGTH_SHORT).show();
                                taskSubmitButton.setText("提交");
                                taskUpdateButton.setVisibility(View.VISIBLE);
                                isConfirmed = true;
                            }
                            else{
                                Toast.makeText(getApplicationContext(), "接受任务失败，请重新提交", Toast.LENGTH_SHORT).show();
                            }
                        }catch (JSONException e){
                            e.printStackTrace();
                        }
                        //progressDialog.hide();
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        //Toast.makeText(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT).show();
                        NoRepeatToast.showToast(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT);
                        //progressDialog.hide();
                    }
                });
    }

    private void submitData(){
        String id = "";
        try{
            id = taskObj.getString("id");
        }catch (Exception e){
            e.printStackTrace();
        }
        String note = taskResultEditText.getText().toString();

        RequestParams params = new RequestParams();
        params.addBodyParameter("username", Config.DEBUG_USERNAME);
        params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
        params.addBodyParameter("task_id", id);
        params.addBodyParameter("note", note);
        //progressDialog.show();

        HttpUtils http = new HttpUtils();
        http.send(HttpRequest.HttpMethod.POST,
                Config.TASK_SUBMIT_URL,
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
                                isSubmitted = true;
                                TaskActivity.this.finish();
                            }
                            else{
                                Toast.makeText(getApplicationContext(), "提交失败，请重新提交", Toast.LENGTH_SHORT).show();
                            }
                        }catch (JSONException e){
                            e.printStackTrace();
                        }
                        //progressDialog.hide();
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        //Toast.makeText(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT).show();
                        NoRepeatToast.showToast(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT);
                        //progressDialog.hide();
                    }
                });
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_task);

        Bundle bundle = this.getIntent().getExtras();
        try {
            taskObj = new JSONObject(bundle.getString("task"));
            position = bundle.getInt("position");
        }catch (Exception e) {
        }
        //progressDialog = new ProgressDialog(TaskActivity.this, R.style.buffer_dialog);
       // progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        //progressDialog.setMessage("数据加载中...");
        //progressDialog.setIndeterminate(false);
        //progressDialog.setCancelable(false);

        ViewUtils.inject(this);
        setValueOfTextView();
    }

    private void setValueOfTextView(){
        String title = "";
        String faultDescription = "";
        String taskMemo = "";
        String taskResult = "";
        String confirmed = "";
        try{
            title = taskObj.getString("title");
            faultDescription = taskObj.getString("description");
            taskMemo = taskObj.getString("memo");
            taskResult = taskObj.getString("note");
            confirmed = taskObj.getString("confirmed");
        }catch (Exception e){
            e.printStackTrace();
        }

        int index = taskMemo.indexOf("审核未通过：");
        if (index < 0){
            index = 0;
        }
        taskMemo = taskMemo.substring(index);

        taskTitleTextView.setText(title);
        taskDescriptionTextView.setText(faultDescription);
        taskMemoTextView.setText(taskMemo);
        taskResultEditText.setText(taskResult);
        if(confirmed.equals("true")) {
            taskSubmitButton.setText("提交");
            taskUpdateButton.setVisibility(View.VISIBLE);
        }else{
            taskSubmitButton.setText("接受任务");
        }
    }

    @Override
    protected  void onDestroy(){
        //progressDialog.dismiss();
        super.onDestroy();
    }

    @Override
    public void finish() {
        Bundle bundle = new Bundle();
        bundle.putInt("position", position);
        bundle.putBoolean("isConfirmed", isConfirmed);
        bundle.putBoolean("isUpdated", isUpdated);
        bundle.putBoolean("isSubmitted", isSubmitted);
        bundle.putString("updatedNote", updatedNote);
        TaskActivity.this.setResult(RESULT_OK, TaskActivity.this.getIntent().putExtras(bundle));

        super.finish();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_task, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            TaskActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
