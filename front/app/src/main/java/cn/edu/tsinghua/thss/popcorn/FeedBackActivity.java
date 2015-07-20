package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EdgeEffect;
import android.widget.EditText;
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


public class FeedBackActivity extends Activity {
    private static String FEEDBACK_URL = Config.LOCAL_IP + "/app/feedback/";

    @ViewInject(R.id.feed_back_text)
    private EditText feedbackEditText;

    @OnClick(R.id.feed_back_submit_btn)
    private void submitFeedbackButtonClick(View v) {
        String feedback = feedbackEditText.getText().toString();
        if(feedback.length() <  4){
            Toast.makeText(getApplicationContext(), "意见不能少于4个字符", Toast.LENGTH_SHORT).show();
        }
        else {
            RequestParams params = new RequestParams();
            params.addBodyParameter("username", Config.DEBUG_USERNAME);
            params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
            params.addBodyParameter("feedback", feedback);
            HttpUtils http = new HttpUtils();
            http.send(HttpRequest.HttpMethod.POST,
                    FEEDBACK_URL,
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
                                    Toast.makeText(getApplicationContext(), "提交成功，感谢您的宝贵意见", Toast.LENGTH_SHORT).show();
                                    FeedBackActivity.this.finish();
                                } else {
                                    Toast.makeText(getApplicationContext(), "提交失败，请重新提交", Toast.LENGTH_SHORT).show();
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
    }
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_feedback);

        ViewUtils.inject(this);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.feedback, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            FeedBackActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
